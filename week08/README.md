# 学科智能问答助手 v1.0

## 功能
- 基于 RAG 的学科问答；支持纯对话 / 基于资料两种模式。

## 怎么装
- pip install -r requirements.txt
- ollama pull qwen2.5:0.5b && ollama pull nomic-embed-text
- 复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY

## 怎么用
- python assistant_v1.py（从 week08_助手v1.0 目录运行）

## 已知问题
- 未启动 Ollama 时本地模式会报错；可设 prefer="api" 走云端。