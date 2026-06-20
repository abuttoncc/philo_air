#!/usr/bin/env python3
"""拾遗员 · 会话转写读取/压实 —— 纯 stdlib，零依赖。

捕获泵的「确定性层」(对应 dpagt 的 conversation_memo)：把 Claude Code 的会话
transcript(.jsonl)压成一段干净的「人说+我说」对话文本，交给 SKILL 的 LLM 层
抽 conviction 候选。**本脚本不调 LLM、不写 wiki**——只读、只压、只记账。

为什么要它:没有它,会话结束即蒸发(1.0 病)。它保证「留痕」即使没人跑 LLM 层。

用法:
  python3 capture.py --list                # 列今天的会话(session id + 轮数 + 是否已捕获)
  python3 capture.py --check               # 有「今天的、够实质的、未捕获」会话 → 退出码 10,否则 0
  python3 capture.py --dump [SID|latest]   # 打印某会话压实后的对话(默认 latest);喂给 LLM 层
  python3 capture.py --mark SID            # 把会话记进 .capture-log(LLM 层落候选后调,防重复捕获)
  VAULT=/path TRANSCRIPTS=/path python3 capture.py ...   # 覆盖路径

退出码: 0=无待捕获 / 10=有待捕获(给 launchd runner 用)。
"""
import sys, os, re, json, glob
from datetime import date, datetime, timezone, timedelta

# 脚本在 .claude/skills/philo-dream/ → 库根上溯 3 层;可被 VAULT 覆盖
VAULT = os.environ.get(
    "VAULT",
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
)
# Claude Code 把本项目会话存在 ~/.claude/projects/<编码过的库路径>/<sid>.jsonl
# 编码规则:把库绝对路径里的 / 和空格等替换成 -。这里直接用已知目录,可被 TRANSCRIPTS 覆盖。
TRANSCRIPTS = os.environ.get(
    "TRANSCRIPTS",
    os.path.expanduser(
        "~/.claude/projects/-Users-jameslee-Documents------James-MacBook-Pro-philo-air"
    ),
)
CAPTURE_LOG = os.path.join(VAULT, "08-Ops", ".capture-log.md")
_BJ = timezone(timedelta(hours=8))
_MIN_USER_TURNS = 3          # 少于这么多轮人类发言 = 不够实质,不值得唤醒 LLM 层
_PER_TURN_TRUNCATE = 6000    # 每轮正文截断,控制 dump 体积


def _bj_today():
    return datetime.now(_BJ).date()


def _text_of(content):
    """user/assistant 的 content 可能是 str 或 content-block 数组。抽人类可读文本,
    工具调用/结果只留极简标记,保持对话主线干净。"""
    if isinstance(content, str):
        return content.strip()
    if not isinstance(content, list):
        return ""
    parts = []
    for b in content:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "text":
            parts.append(b.get("text", "").strip())
        elif t == "tool_use":
            parts.append(f"[调用工具:{b.get('name', '?')}]")
        elif t == "tool_result":
            parts.append("[工具结果]")
        elif t == "thinking":
            continue  # 思考不入捕获
    return "\n".join(p for p in parts if p).strip()


def _iter_lines(path):
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except ValueError:
                    continue
    except OSError:
        return


def _session_meta(path):
    """轻扫一个 jsonl,返回 {sid, user_turns, assistant_turns, started, first_user}."""
    sid = os.path.splitext(os.path.basename(path))[0]
    user_turns = asst_turns = 0
    started = None
    first_user = ""
    for obj in _iter_lines(path):
        if obj.get("isSidechain"):        # 子智能体支线,不算主线
            continue
        ts = obj.get("timestamp")
        if ts and not started:
            started = ts
        typ = obj.get("type")
        if typ == "user":
            msg = obj.get("message", {})
            txt = _text_of(msg.get("content"))
            # 跳过纯工具结果回灌的 user 行(没有真人文字)
            if txt and not txt.startswith("[工具结果]"):
                user_turns += 1
                if not first_user:
                    first_user = txt[:60].replace("\n", " ")
        elif typ == "assistant":
            asst_turns += 1
    return {"sid": sid, "path": path, "user_turns": user_turns,
            "assistant_turns": asst_turns, "started": started, "first_user": first_user}


def _today_sessions():
    paths = glob.glob(os.path.join(TRANSCRIPTS, "*.jsonl"))
    out = []
    today = _bj_today()
    for p in paths:
        mt = datetime.fromtimestamp(os.path.getmtime(p), _BJ).date()
        if mt == today:
            out.append(_session_meta(p))
    out.sort(key=lambda m: m["started"] or "", reverse=True)
    return out


def _captured_sids():
    if not os.path.exists(CAPTURE_LOG):
        return set()
    sids = set()
    with open(CAPTURE_LOG, encoding="utf-8") as f:
        for line in f:
            m = re.search(r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b", line)
            if m:
                sids.add(m.group(1))
    return sids


def _resolve(which):
    paths = sorted(glob.glob(os.path.join(TRANSCRIPTS, "*.jsonl")),
                   key=os.path.getmtime, reverse=True)
    if not paths:
        return None
    if which in (None, "latest"):
        return paths[0]
    for p in paths:
        if os.path.splitext(os.path.basename(p))[0] == which:
            return p
    return None


def cmd_list():
    captured = _captured_sids()
    rows = _today_sessions()
    print(json.dumps({
        "today": str(_bj_today()),
        "sessions": [
            {**{k: m[k] for k in ("sid", "user_turns", "assistant_turns", "started", "first_user")},
             "captured": m["sid"] in captured,
             "substantive": m["user_turns"] >= _MIN_USER_TURNS}
            for m in rows
        ],
    }, ensure_ascii=False, indent=2))


def cmd_check():
    captured = _captured_sids()
    pending = [m for m in _today_sessions()
               if m["user_turns"] >= _MIN_USER_TURNS and m["sid"] not in captured]
    sys.exit(10 if pending else 0)


def cmd_dump(which):
    path = _resolve(which)
    if not path:
        print("(无可读 transcript)", file=sys.stderr)
        sys.exit(1)
    sid = os.path.splitext(os.path.basename(path))[0]
    print(f"# 会话转写 · session {sid}\n")
    n = 0
    for obj in _iter_lines(path):
        if obj.get("isSidechain"):
            continue
        typ = obj.get("type")
        if typ not in ("user", "assistant"):
            continue
        txt = _text_of(obj.get("message", {}).get("content"))
        if not txt or txt == "[工具结果]":
            continue
        who = "人" if typ == "user" else "我"
        ts = (obj.get("timestamp") or "")[:16]
        if len(txt) > _PER_TURN_TRUNCATE:
            txt = txt[:_PER_TURN_TRUNCATE] + " …(截断)"
        print(f"\n## {who} {ts}\n{txt}")
        n += 1
    if n == 0:
        print("(空会话)", file=sys.stderr)


def cmd_mark(sid):
    os.makedirs(os.path.dirname(CAPTURE_LOG), exist_ok=True)
    stamp = datetime.now(_BJ).strftime("%Y-%m-%d %H:%M")
    header_needed = not os.path.exists(CAPTURE_LOG)
    with open(CAPTURE_LOG, "a", encoding="utf-8") as f:
        if header_needed:
            f.write("# 捕获账本 (.capture-log)\n\n"
                    "> 拾遗员落候选后逐行追加,防重复捕获。append-only。\n\n")
        f.write(f"- {stamp} · {sid}\n")
    print(f"marked {sid}")


def main():
    args = sys.argv[1:]
    if not args or args[0] == "--list":
        cmd_list()
    elif args[0] == "--check":
        cmd_check()
    elif args[0] == "--dump":
        cmd_dump(args[1] if len(args) > 1 else "latest")
    elif args[0] == "--mark" and len(args) > 1:
        cmd_mark(args[1])
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
