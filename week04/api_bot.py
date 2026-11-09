import os
import sys
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

BASE_URL = "https://api.deepseek.com/v1"
MODEL = "deepseek-chat"
_client = None

def get_client():
    global _client
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        return None
    _client = OpenAI(base_url=BASE_URL, api_key=key)
    return _client

def ask(question, temperature=0.7, max_tokens=800):
    client = get_client()
    if client is None:
        raise Exception("未读取到DEEPSEEK_API_KEY密钥")
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content": question}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content, resp.usage

if __name__ == "__main__":
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：未设置 DEEPSEEK_API_KEY。请配置本地 .env 文件。")
        sys.exit(1)

    if len(sys.argv) >=2:
        user_q = " ".join(sys.argv[1:])
    else:
        user_q = "把字句的教学难点有哪些"

    answer, usage_info = ask(user_q, temperature=0.7, max_tokens=800)
    print(f"问题：{user_q}")
    print(f"回答：{answer}")

    # 写入对话日志 chat_log.txt
    log_line = f"\n=====问题=====\n{user_q}\n=====回答=====\n{answer}\n"
    with open("chat_log.txt","a",encoding="utf‑8") as f:
        f.write(log_line)