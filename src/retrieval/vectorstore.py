import os
from typing import List, Tuple
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from functools import lru_cache

EMBED_MODEL = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K = 6


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Load embedding model once and cache it."""
    return HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore(search_results: List[dict]) -> FAISS:
    """
    Chunk all fetched content and index into an in-memory FAISS store.
    Each chunk carries metadata: title, url.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " "],
    )

    docs: List[Document] = []
    for result in search_results:
        text = result.get("content") or result.get("snippet", "")
        if not text.strip():
            continue
        chunks = splitter.split_text(text)
        for chunk in chunks:
            docs.append(Document(
                page_content=chunk,
                metadata={
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "snippet": result.get("snippet", ""),
                },
            ))

    if not docs:
        raise ValueError("No content to index — all search results were empty.")

    embeddings = get_embeddings()
    return FAISS.from_documents(docs, embeddings)


def retrieve(vectorstore: FAISS, query: str, k: int = TOP_K) -> List[Tuple[str, dict]]:
    """
    Retrieve top-k chunks relevant to query.
    Returns list of (chunk_text, metadata) tuples.
    """
    results = vectorstore.similarity_search(query, k=k)
    return [(doc.page_content, doc.metadata) for doc in results]
