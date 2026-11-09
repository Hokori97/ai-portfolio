# W4课后作业2：机器人增加多轮追问功能
### 实现思路
维护一个messages列表保存完整对话历史。
- 用户提问，把{"role":"user","content":用户输入}追加进messages；
- 调用API拿到assistant回答，再把{"role":"assistant","content":模型输出}追加进messages；
- 下一轮请求直接把完整messages传给接口，模型就能记住上下文。

### 关键改动点
1.不再每次只传单条user消息；messages持续累积会话上下文。
2.增加循环输入，输入exit退出会话。
3.保留temperature、max_tokens参数，保留日志写入逻辑。

### 核心片段示例
messages = []
while True:
    q = input("请输入问题(exit退出)：")
    if q.strip() == "exit":
        break
    messages.append({"role":"user","content": q})
    resp = client.chat.completions.create(model=MODEL,messages=messages)
    ans = resp.choices[0].message.content
    print(ans)
    messages.append({"role":"assistant","content": ans})