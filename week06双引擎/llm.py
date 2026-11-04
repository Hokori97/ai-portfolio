import requests
import time
from openai import OpenAI

# ========= 配置区 =========
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:0.5b"

# DeepSeek 配置
api_client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="xxx"
)
DEEPSEEK_MODEL = "deepseek-chat"
# ===========================

def call_ollama(prompt: str):
    """调用本地Ollama引擎"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["response"]


def call_api(prompt: str):
    """调用DeepSeek远程API"""
    response = api_client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[{"role": "user", "content": prompt}],
        timeout=15
    )
    return response.choices[0].message.content


def ask(prompt: str, prefer="local"):
    """统一入口，prefer可选 local / api，失败自动双向切换"""
    start_time = time.time()
    if prefer == "local":
        try:
            print("【优先尝试：本地Ollama】")
            res = call_ollama(prompt)
            cost = round(time.time() - start_time, 2)
            return {"engine": "ollama", "content": res, "time_cost": cost}
        except Exception as e:
            print(f"本地Ollama调用失败！原因：{e}，自动切换到DeepSeek API")
            res = call_api(prompt)
            cost = round(time.time() - start_time, 2)
            return {"engine": "api", "content": res, "time_cost": cost}

    elif prefer == "api":
        try:
            print("【优先尝试：DeepSeek远程API】")
            res = call_api(prompt)
            cost = round(time.time() - start_time, 2)
            return {"engine": "api", "content": res, "time_cost": cost}
        except Exception as e:
            print(f"DeepSeek API调用失败！原因：{e}，自动切换本地Ollama")
            res = call_ollama(prompt)
            cost = round(time.time() - start_time, 2)
            return {"engine": "ollama", "content": res, "time_cost": cost}


if __name__ == "__main__":
    # 三条路径共用同一个问题
    question = "解释什么是区别词，举两个例子"
    print("=====路径1：Ollama开启，prefer=local=====")
    r1 = ask(question, prefer="local")
    print(r1)

    print("\n=====路径2：关闭Ollama，prefer=local=====")
    r2 = ask(question, prefer="local")
    print(r2)

    print("\n=====路径3：Ollama开启，prefer=api=====")
    r3 = ask(question, prefer="api")
    print(r3)
