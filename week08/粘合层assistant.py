import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import weekpath
weekpath.load_env()

from llm import LLM
from rag_qa import retrieve, build_prompt

llm = LLM()
SYSTEM_HINT = "你是国际中文教学助手，面向 HSK3–4 学习者，回答需给出依据。"

def answer(question, use_rag=True, prefer="local"):
    if use_rag:
        ctx = retrieve(question)
        prompt = SYSTEM_HINT + "\n" + build_prompt(question, ctx)
    else:
        prompt = SYSTEM_HINT + "\n" + question
    return llm.ask(prompt, prefer=prefer)


if __name__ == "__main__":
    for q in ["把字句的教学难点有哪些",
              "HSK4 词汇量要求是多少",
              "《愚公移山》可以设计什么课堂活动"]:
        print("Q:", q)
        try:
            print("A:", answer(q))
        except Exception as e:
            print("A: [运行失败] %s" % e)
        print("-" * 40)
