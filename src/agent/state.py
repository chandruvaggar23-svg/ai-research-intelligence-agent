from typing import TypedDict, List, Dict, Any, Optional


class SearchResult(TypedDict):
    title: str
    url: str
    snippet: str
    content: str


class ReportSection(TypedDict):
    heading: str
    content: str


class ResearchState(TypedDict):
    # Input
    query: str

    # Planning
    sub_queries: List[str]
    research_angle: str           # Key perspective / framing

    # Search & Retrieval
    search_results: List[SearchResult]
    retrieved_chunks: List[str]   # FAISS-retrieved relevant chunks
    sources: List[Dict[str, str]] # Deduplicated sources for citations

    # Synthesis
    draft_synthesis: str          # First-pass synthesis
    final_report: str             # Structured markdown report

    # Control flow
    iteration: int
    max_iterations: int
    should_refine: bool
    status: str                   # Human-readable step description
    error: Optional[str]
