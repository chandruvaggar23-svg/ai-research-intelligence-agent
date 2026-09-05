# 🔬 ResearchIQ — AI Research Intelligence Agent

> An AI-powered research workspace that turns complex questions into structured, evidence-backed reports through web search, semantic retrieval, LLM synthesis, and iterative quality checks.

## ✨ Overview

ResearchIQ is an end-to-end AI research agent designed to automate the research workflow.

Instead of manually searching multiple pages and combining the findings, the agent:

1. Breaks a research question into focused sub-queries.
2. Searches the web using DuckDuckGo.
3. Fetches and cleans relevant page content.
4. Splits the content into searchable chunks.
5. Builds an in-memory FAISS vector index.
6. Retrieves the most relevant information for the question.
7. Uses a Groq-hosted LLM to synthesize the findings.
8. Generates a structured Markdown research report.
9. Performs a quality check and can refine the research when needed.

## 🚀 Key Features

- **Autonomous query planning** — decomposes complex questions into 3–5 focused sub-queries.
- **Web research pipeline** — searches DuckDuckGo and fetches visible page content.
- **RAG-style retrieval** — uses Hugging Face embeddings with FAISS for semantic retrieval.
- **LLM synthesis** — generates dense, factual synthesis from retrieved evidence.
- **Structured reports** — produces executive summary, findings, conclusion, takeaways, and sources.
- **Iterative refinement** — quality-checks the generated report and performs another research pass when required.
- **Interactive dashboard** — Streamlit interface for queries, model/settings, sources, research plan, retrieved chunks, and report export.
- **Secure API-key workflow** — API credentials are supplied through environment variables or the UI rather than hard-coded.

## 🧠 Architecture

```text
                         ┌──────────────────────┐
                         │   User Research      │
                         │       Query          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Query Planning     │
                         │   LangGraph Node     │
                         └──────────┬───────────┘
                                    │
                         sub-queries + angle
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Web Search        │
                         │    DuckDuckGo        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Content Extraction   │
                         │ Requests + BeautifulSoup
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Chunk + Embed        │
                         │ Hugging Face         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ FAISS Vector Store   │
                         │ Semantic Retrieval   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ LLM Synthesis        │
                         │ Groq + LLM           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Report Generation    │
                         │ Structured Markdown  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Quality Check      │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                      Refine                  End
                         │
                         └──────► Search
```

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| Agent orchestration | LangGraph |
| LLM | Groq / LLaMA-compatible ChatGroq models |
| Search | DuckDuckGo |
| Retrieval | FAISS |
| Embeddings | Hugging Face `all-MiniLM-L6-v2` |
| Web extraction | Requests + BeautifulSoup |
| Environment management | python-dotenv |

## 📁 Project Structure

```text
ai-research-intelligence-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
└── src/
    ├── __init__.py
    │
    ├── agent/
    │   ├── __init__.py
    │   ├── graph.py
    │   ├── nodes.py
    │   └── state.py
    │
    ├── llm/
    │   ├── __init__.py
    │   └── groq_client.py
    │
    ├── report/
    │   ├── __init__.py
    │   └── generator.py
    │
    ├── retrieval/
    │   ├── __init__.py
    │   └── vectorstore.py
    │
    └── search/
        ├── __init__.py
        └── duckduckgo.py
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-research-intelligence-agent.git
cd ai-research-intelligence-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Groq API key

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Then add your API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env` or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 Agent Workflow

The LangGraph workflow is organized into modular nodes:

```text
plan
  ↓
search
  ↓
retrieve
  ↓
synthesize
  ↓
report
  ↓
quality_check
  ├── END
  └── refine → search
```

This modular design makes the research process easier to understand, test, and extend.

## 📊 Dashboard

The Streamlit interface provides:

- Research query input
- Example research prompts
- Search-result configuration
- Refinement iteration controls
- AI model configuration
- Research progress indicators
- Research-plan/sub-query display
- Source list and snippets
- Retrieved FAISS chunks
- Generated report
- Markdown report download
- Raw agent state inspection

## 🔐 Security

- Keep API keys in `.env` or Streamlit secrets.
- Do not commit `.env`.
- Do not paste API keys into source code.
- Rotate any key that has accidentally been exposed.

## 🚧 Future Improvements

- Add source credibility scoring.
- Add citation verification.
- Add persistent vector storage.
- Add PDF/document ingestion.
- Add multi-source citation tracking.
- Add report export to PDF/DOCX.
- Add automated evaluation metrics for retrieval and answer quality.
- Deploy the application with a managed secrets configuration.

## 👨‍💻 Project

**ResearchIQ — AI Research Intelligence Agent**

Built as an end-to-end AI/ML project demonstrating agent orchestration, RAG-style retrieval, web research, LLM synthesis, and interactive application development.
