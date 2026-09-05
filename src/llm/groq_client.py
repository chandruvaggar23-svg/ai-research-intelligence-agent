import os
from functools import lru_cache
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage


GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")



@lru_cache(maxsize=1)
def get_llm(temperature: float = 0.1) -> ChatGroq:
    """Return a cached ChatGroq instance."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Copy .env.example to .env and add your key.")
    return ChatGroq(
        model=GROQ_MODEL,
        temperature=temperature,
        groq_api_key=api_key,
        max_retries=3,
    )


def chat(system: str, user: str, temperature: float = 0.1) -> str:
    """Single-turn chat with Groq LLaMA."""
    llm = get_llm(temperature)
    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]
    response = llm.invoke(messages)
    return response.content.strip()


def stream_chat(system: str, user: str, temperature: float = 0.1):
    """Streaming chat — yields text chunks."""
    llm = get_llm(temperature)
    messages = [
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]
    for chunk in llm.stream(messages):
        if chunk.content:
            yield chunk.content
