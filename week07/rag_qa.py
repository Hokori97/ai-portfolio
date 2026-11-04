# 依赖：
# pip install langchain langchain-community langchain-chroma langchain-ollama chromadb
# ollama pull nomic-embed-text
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath
weekpath.load_env()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from llm import LLM

CORPUS = weekpath.data_path("等级标准清单.txt")
PERSIST = weekpath.root_path("chroma_db")
_retriever = None

def get_retriever(k=3, rebuild=False):
    """延迟构建，只有真正检索时才建库；库已存在且不重建，直接复用"""
    global _retriever
    if _retriever is not None and not rebuild:
        return _retriever
    emb = OllamaEmbeddings(model="nomic-embed-text")
    if not rebuild and os.path.exists(PERSIST):
        db = Chroma(persist_directory=PERSIST, embedding_function=emb)
    else:
        docs = TextLoader(CORPUS, encoding="utf-8").load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = splitter.split_documents(docs)
        db = Chroma.from_documents(splits, emb, persist_directory=PERSIST)
    _retriever = db.as_retriever(search_kwargs={"k": k})
    return _retriever

def retrieve(question):
    return "\n".join([d.page_content for d in get_retriever().invoke(question)])

def build_prompt(question, ctx):
    return f"""根据以下资料回答问题，资料中没有的内容就如实说“资料中未提及”：
【资料片段】
{ctx}
【问题】
{question}
"""

if __name__ == "__main__":
    llm = LLM()
    q = " ".join(sys.argv[1:]) or "HSK4 要求掌握哪些语法点？"
    ctx = retrieve(q)
    print("【检索片段】\n", ctx[:300], "\n----")
    # 隐私任务 prefer="local"，复杂任务 prefer="api"
    print(llm.ask(build_prompt(q, ctx), prefer="local"))
