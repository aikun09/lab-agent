from typing import List

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.api.types import EmbeddingFunction, Embeddings
from openai import OpenAI

from app.config import BASE_DIR, settings

KB_DIR = BASE_DIR / "data" / "kb"
CHROMA_DIR = BASE_DIR / "data" / "chroma"

_collection = None


class OnlineEmbeddingFunction(EmbeddingFunction):
    """调硅基流动 API 算向量——零下载"""

    def __init__(self):
        if not settings.EMBEDDING_API_KEY:
            raise RuntimeError("未配置 EMBEDDING_API_KEY")
        self._client = OpenAI(
            api_key=settings.EMBEDDING_API_KEY,
            base_url=settings.EMBEDDING_BASE_URL,
        )
        self._model = settings.EMBEDDING_MODEL

    def __call__(self, input: List[str]) -> Embeddings:
        res = self._client.embeddings.create(model=self._model, input=input)
        return [item.embedding for item in res.data]


def get_collection() -> Collection:
    """向量库的初始化"""
    global _collection
    if _collection is not None:
        return _collection
    KB_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    col = client.get_or_create_collection(
        name="lab_kb", embedding_function=OnlineEmbeddingFunction()
    )
    if col.count() == 0:
        ids = []
        docs = []
        metas = []
        for path in sorted(KB_DIR.glob("*.md")):  # 按文件名排序扫描所有 .md
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            docs.append(text)
            ids.append(path.stem)
            metas.append({"source": path.name})
        if docs:
            col.add(
                ids=ids,
                documents=docs,
                metadatas=metas,
            )
    _collection = col
    return col


def search(query: str):
    """根据关键字去检索向量库"""

    col = get_collection()
    if col.count() == 0:
        return ""
    limit = min(5, col.count())
    res = col.query(query_texts=[query], n_results=limit)
    docs = (res.get("documents") or [[]])[0]  # [list]
    metas = (res.get("metadatas") or [[]])[0]  # [list]
    distances = (res.get("distances") or [])[0]  # [list]
    """
    以下是检索出来的资料：
    [预约规则.md]

    #实验室预约规则...

    
    [安全规范.md]

    安全规范...
    """
    score_parts = []
    for doc, metas, dist in zip(docs, metas, distances):
        # 0-1 越接近1表示越相关
        score = 1 / (1 + dist)
        if score < 0.5:
            continue
        name = (metas or {}).get("source") or ""
        score_parts.append({"score": score, "content": f"[{name}]\n{doc}"})
    score_parts.sort(key=lambda x: x["score"], reverse=True)
    final_parts = [item["content"] for item in score_parts[:2]]
    return "\n\n".join(final_parts)
