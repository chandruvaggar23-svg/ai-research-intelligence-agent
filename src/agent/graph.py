"""
ResearchIQ LangGraph Pipeline
─────────────────────────────
Flow:
  START
    ↓
  plan          → decompose query into sub-queries
    ↓
  search        → DuckDuckGo search + content scraping
    ↓
  retrieve      → FAISS indexing + semantic retrieval
    ↓
  synthesize    → Groq LLaMA first-pass synthesis
    ↓
  report        → generate structured markdown report
    ↓
  quality_check → pass/fail decision
    ↓          ↘
  END          refine → search → retrieve → synthesize → report → END
"""

from langgraph.graph import StateGraph, END
from src.agent.state import ResearchState
from src.agent.nodes import (
    plan_node,
    search_node,
    retrieve_node,
    synthesize_node,
    report_node,
    quality_check_node,
    refine_node,
)


def route_after_quality(state: ResearchState) -> str:
    """Conditional edge: refine or end."""
    if state.get("should_refine", False):
        return "refine"
    return END


def build_graph() -> StateGraph:
    """Assemble and compile the ResearchIQ LangGraph."""
    graph = StateGraph(ResearchState)

    # Register nodes
    graph.add_node("plan", plan_node)
    graph.add_node("search", search_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("report", report_node)
    graph.add_node("quality_check", quality_check_node)
    graph.add_node("refine", refine_node)

    # Linear edges
    graph.set_entry_point("plan")
    graph.add_edge("plan", "search")
    graph.add_edge("search", "retrieve")
    graph.add_edge("retrieve", "synthesize")
    graph.add_edge("synthesize", "report")
    graph.add_edge("report", "quality_check")

    # Conditional edge from quality_check
    graph.add_conditional_edges(
        "quality_check",
        route_after_quality,
        {"refine": "refine", END: END},
    )

    # Refinement loops back into search (gets new docs), re-indexes, re-synthesizes
    graph.add_edge("refine", "search")

    return graph.compile()


# Singleton compiled graph
_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


def run_research(query: str, max_iterations: int = 2) -> ResearchState:
    """
    Run the full research pipeline for a given query.
    Returns the final state dict.
    """
    graph = get_graph()
    initial_state: ResearchState = {
        "query": query,
        "sub_queries": [],
        "research_angle": "",
        "search_results": [],
        "retrieved_chunks": [],
        "sources": [],
        "draft_synthesis": "",
        "final_report": "",
        "iteration": 0,
        "max_iterations": max_iterations,
        "should_refine": False,
        "status": "Starting research…",
        "error": None,
    }
    return graph.invoke(initial_state)
