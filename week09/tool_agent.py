# W9 手写最小工具调用循环（课堂作业，当堂交付）
# 依赖：pip install openai python-dotenv
import os
import csv
import sys
import ast
import json
import re
import operator
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402
weekpath.load_env()
import openai  # noqa: E402

VOCAB = weekpath.data_path("生词表.csv")
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
_client = None

def get_client():
    global _client
    if _client is None:
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY，请先在 .env 中填写")
        base = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        _client = openai.OpenAI(base_url=base, api_key=key)
    return _client

# 工具1：获取当前系统时间
def get_time():
    return str(datetime.datetime.now())

# 工具2：安全计算器 AST白名单，禁止eval
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError("只允许数字与 + - * / ** % 运算")

def calc(expr):
    """安全四则运算工具，禁止裸eval"""
    try:
        return str(_eval_node(ast.parse(str(expr), mode="eval")))
    except ZeroDivisionError:
        return "错误：除数为 0"
    except Exception as e:
        return "拒绝计算：%s" % e

# 工具3：查询词汇HSK等级
def hsk_level(word):
    with open(VOCAB, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["词汇"].strip() == str(word).strip():
                return f"{word} 是 {row['HSK等级']} 级"
    return f"未找到 {word}"

TOOLS = {"get_time": get_time, "calc": calc, "hsk_level": hsk_level}

SYS = ("你是国际中文助教。可用工具只有这 3 个：get_time（查当前时间，无参数）、"
       "calc（四则运算，如 calc('120+45')）、hsk_level（查生词 HSK 等级，如 hsk_level('商量')）。"
       '如需调用，只输出一行 JSON，格式：{"tool": "工具名", "args": [参数]}；'
       "一次可调用多个工具，绝不编造不存在的工具名；无需工具时直接回答。")

def parse_calls(txt):
    """容错解析：剥离markdown代码围栏，正则兜底抓取JSON块，兼容多工具并列输出"""
    s = (txt or "").strip()
    s = s.replace("```json", "").replace("```", "").strip()
    try:
        obj = json.loads(s)
        return [obj] if isinstance(obj, dict) else []
    except Exception:
        m = re.search(r"\{.*\}", s, re.S)
        if m:
            try:
                obj = json.loads(m.group())
                if isinstance(obj, dict):
                    return [obj]
            except Exception:
                pass
        calls = []
        for blk in re.findall(r"\{[^{}]*\}", s):
            try:
                obj = json.loads(blk)
            except Exception:
                continue
            if isinstance(obj, dict):
                calls.append(obj)
        return calls

def run(user_msg, max_calls=2):
    msgs = [{"role": "system", "content": SYS}, {"role": "user", "content": user_msg}]
    for _ in range(max_calls):
        txt = get_client().chat.completions.create(
            model=MODEL, messages=msgs).choices[0].message.content
        calls = [c for c in parse_calls(txt)
                 if isinstance(c.get("tool"), str) and c.get("tool") in TOOLS]
        if not calls:
            return txt
        results = []
        for call in calls:
            args = call.get("args") or []
            if not isinstance(args, list):
                results.append(f"工具参数格式错误：{repr(args)}")
                continue
            try:
                results.append(f"{call['tool']}{repr(args)} → {TOOLS[call['tool']](*args)}")
            except Exception as e:
                results.append(f"工具执行失败：{e}")
        msgs += [{"role": "assistant", "content": txt},
                 {"role": "user", "content": f"工具返回：{'；'.join(results)}。请据此作答。"}]
    return get_client().chat.completions.create(
        model=MODEL, messages=msgs).choices[0].message.content

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "请告诉我决定这个词语的HSK等级，同时帮我算出12*28等于多少"
    print("用户输入：", q)
    print("助手：", run(q))