# 实验3 MCP实践记录【回家作业1】
## 1. 配置记录
- 使用客户端：课程最小Python客户端 demo_client.py
- MCP服务端配置JSON
```json
{"mcpServers": {"hsk-tools": {"command": "python", "args": ["hsk_mcp_server.py"]}}}
```

## 2.调用证据
1. 获取工具列表输出：['hsk_level', 'list_by_level', 'count_by_level']
2. hsk_level测试调用
输入参数 {"word":"把"}，返回结果：把 -> 3 级
3. list_by_level测试调用示例
输入参数 {"level":"3"}，返回对应HSK3级词汇列表。
4. 新增工具 count_by_level 调用证据
输入参数 {"level":"3"}，返回该等级词汇总数量。

## 3.调用辨析

1. Function Calling（模型侧）：属于模型侧调用机制，让模型点名决定调用哪个工具；课程示例W9 tool_agent.py的TOOLS字典。一句话：模型说“我要查等级”。

2. MCP（工具侧协议）：工具侧统一协议，规定工具如何被发现、描述、调用；课程示例本次hsk_mcp_server.py。一句话：定义查等级工具长什么样、在哪。⚠MCP不是量化、模型压缩。

3. 普通 API 调用（程序侧）：程序直接向服务发起请求，没有模型参与决策；课程示例W4 week4_api_bot.py调用DeepSeek。一句话：代码直接向服务索要答案。