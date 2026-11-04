# W5课后作业1：Ollama官方文档阅读笔记

阅读了 Ollama 官方文档 Model 管理与 API 两节，记录 3 条以前不知道的用法：

## 1. 自定义 Modelfile 固化系统提示词
可以新建一个 Modelfile，用 FROM 指定基础模型，用 SYSTEM 写死系统提示词，
然后 `ollama create my-bot -f Modelfile`，以后直接 `ollama run my-bot` 就自带角色设定，
不用每次在对话开头重复粘贴长提示词。比如做对外汉语助教，可以把"你是HSK辅导老师"写进 SYSTEM。

## 2. temperature 等参数在 API 请求里传，不是写在模型名里
调 /api/chat 时，json 里可以带 options 字段：
{
  "model": "qwen2.5:0.5b",
  "messages": [...],
  "options": {"temperature": 0.2, "num_predict": 200}
}
temperature 调低适合出题、术语解释；num_predict 限制输出长度，防止小模型啰嗦或截断异常。
之前以为参数只能在命令行 /set 里改，其实 Python 直连时每次请求都能动态传。

## 3. keep_alive 参数控制模型在内存里驻留多久
默认模型加载后会在内存里驻留 5 分钟，之后自动卸载。
如果做课堂连续提问，可以在请求里加 "keep_alive": "30m"，让模型常驻，
避免每问一次都重新加载 5 秒。如果想立刻释放内存，传 "keep_alive": 0。