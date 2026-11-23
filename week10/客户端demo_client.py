import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(command="python", args=["hsk_mcp_server.py"])
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            # 第一步：发现工具
            tools = await s.list_tools()
            print("工具列表：", [t.name for t in tools.tools])
            # 第二步：调用 hsk_level 测试词语“把”
            res = await s.call_tool("hsk_level", {"word": "把"})
            print("调用结果：", res.content[0].text)

asyncio.run(main())