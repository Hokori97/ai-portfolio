# W10 自定义 MCP 服务器【回家作业2：新增count_by_level工具】
# 依赖：pip install "mcp[cli]"
import os
import csv
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402
weekpath.load_env()

try:
    from mcp.server.fastmcp import FastMCP      # mcp 1.x
except ImportError:
    try:
        from mcp.server import MCPServer as FastMCP   # mcp 2.x
    except ImportError:
        raise SystemExit(
            "未找到 MCP 服务端库。请先安装：pip install \"mcp[cli]\"\n")

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

@mcp.tool()
def count_by_level(level: str) -> str:
    """统计某一HSK等级的词汇总数量。
    :param level: HSK等级字符串，例如"3"
    :return: 返回该等级词汇的数目
    """
    count = len([row for row in _rows() if row["HSK等级"] == str(level).strip()])
    return f"HSK {level} 级词汇总数：{count}"

if __name__ == "__main__":
    mcp.run()