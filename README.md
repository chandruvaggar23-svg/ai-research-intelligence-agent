# ResearchIQ — AI Research Agent

A RAG-powered research agent that autonomously searches the web, indexes sources with FAISS, and synthesizes structured research reports using Groq-hosted LLaMA models — orchestrated with LangGraph.

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                  LangGraph Pipeline                  │
│                                                     │
│  plan ──► search ──► retrieve ──► synthesize        │
│                                       │             │
│   ┌─────────────── refine ◄──┐    report            │
│   │   (if quality fails)     │       │              │
│   └──────────────────────────┘  quality_check       │
│                                       │              │
│                                      END             │
└─────────────────────────────────────────────────────┘
    │
    ▼
Structured Markdown Report
```

## Pipeline Steps

| Step | Description | Tool |
|------|-------------|------|
| **Plan** | Decompose query into 3–5 sub-queries | Groq LLaMA |
| **Search** | Search web for each sub-query | DuckDuckGo API |
| **Retrieve** | Chunk + index results, semantic retrieval | FAISS + sentence-transformers |
| **Synthesize** | Merge retrieved chunks into dense paragraphs | Groq LLaMA |
| **Report** | Generate structured Markdown report | Groq LLaMA |
| **Quality Check** | Verify report completeness | Groq LLaMA |
| **Refine** *(optional)* | Search supplementary sources, re-synthesize | DuckDuckGo + FAISS |

## Stack

| Component | Library |
|-----------|---------|
| Agent orchestration | LangGraph |
| LLM | Groq (llama-3.3-70b-versatile) |
| Vector store | FAISS (CPU) |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Web search | duckduckgo-search |
| Web scraping | requests + BeautifulSoup4 |
| UI | Streamlit |

## Setup

### 1. Clone & install
```bash
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env and set your GROQ_API_KEY
```

Get a free Groq API key at https://console.groq.com

### 3. Run
```bash
streamlit run app.py
```

Opens at http://localhost:8501

## Project Structure

```
researchiq/
├── app.py                        # Streamlit UI
├── requirements.txt
├── .env.example
└── src/
    ├── agent/
    │   ├── state.py              # ResearchState TypedDict
    │   ├── nodes.py              # LangGraph node functions
    │   └── graph.py              # Graph definition + runner
    ├── retrieval/
    │   └── vectorstore.py        # FAISS build + retrieval
    ├── search/
    │   └── duckduckgo.py         # DDG search + web scraper
    ├── llm/
    │   └── groq_client.py        # Groq LLaMA wrapper
    └── report/
        └── generator.py          # Synthesis + report generation
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | — | Required |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Model to use |
| `EMBED_MODEL` | `all-MiniLM-L6-v2` | Embedding model |
| `MAX_SEARCH_RESULTS` | `5` | Results per sub-query |
| `MAX_ITERATIONS` | `2` | Refinement iterations |
| `CHUNK_SIZE` | `500` | FAISS chunk size (chars) |
| `CHUNK_OVERLAP` | `50` | Chunk overlap |

## Author
Chandru Vaggar | 1KI23CS033 | Kalpataru Institute of Technology
