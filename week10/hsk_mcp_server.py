# W10 自定义 MCP 服务器：查 HSK 词汇等级
# 依赖：pip install "mcp[cli]"      （mcp 1.x 与 2.x 都能跑，下面做了版本自适应）
# 运行：python hsk_mcp_server.py
import os
import csv
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  数据路径 + 加载 .env
weekpath.load_env()
# mcp 2.x 起 FastMCP 改名为 MCPServer，1.x 的导入路径已移除。
# 教学材料不能因为库升级就跑不起来，这里做版本自适应，并在都不可用时给出可操作提示。
try:
    from mcp.server.fastmcp import FastMCP      # mcp 1.x
except ImportError:
    try:
        from mcp.server import MCPServer as FastMCP   # mcp 2.x
    except ImportError:
        raise SystemExit(
            "未找到 MCP 服务端库。请先安装：pip install \"mcp[cli]\"\n"
            "（若使用 mcp 2.x，本文件会自动改用 MCPServer，无需改代码。）")
VOCAB = weekpath.data_path("生词表.csv")
mcp = FastMCP("hsk-tools")
def _rows():
    with open(VOCAB, encoding="utf-8") as f:
        return list(csv.DictReader(f))
@mcp.tool()
def hsk_level(word: str) -> str:
    """查询某个词属于 HSK 几级。"""
    for row in _rows():
        if row["词汇"].strip() == str(word).strip():
            return "%s -> %s 级" % (word, row["HSK等级"])
    return "未找到 %s" % word
@mcp.tool()
def list_by_level(level: str) -> str:
    """列出某一 HSK 等级的全部词汇。"""
    out = [row["词汇"] for row in _rows() if row["HSK等级"] == str(level).strip()]
    return "、".join(out) if out else "该等级暂无词汇"
if __name__ == "__main__":
    mcp.run()
# 客户端配置示例（以各客户端官方文档为准）：
# {"mcpServers": {"hsk-tools": {"command": "python", "args": ["hsk_mcp_server.py"]}}}
# 教学提醒：MCP = Model Context Protocol（模型上下文协议），
# 与第 5 讲的"量化(Quantization)"不是一回事，不要混用缩写。