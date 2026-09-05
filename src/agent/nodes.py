"""
LangGraph node functions for the ResearchIQ pipeline.
Each node receives the full ResearchState and returns a partial update dict.
"""
from typing import Dict, Any, List
from src.agent.state import ResearchState
from src.search.duckduckgo import search_and_fetch
from src.retrieval.vectorstore import build_vectorstore, retrieve
from src.report.generator import plan_queries, generate_synthesis, generate_report, check_quality


# ── Node 1: Query Planning ───────────────────────────────────────────────────

def plan_node(state: ResearchState) -> Dict[str, Any]:
    """Decompose the main query into sub-queries and identify research angle."""
    query = state["query"]
    result = plan_queries(query)
    return {
        "sub_queries": result["sub_queries"],
        "research_angle": result["research_angle"],
        "status": f"Planning complete: {len(result['sub_queries'])} sub-queries identified",
        "error": None,
    }


# ── Node 2: Web Search ───────────────────────────────────────────────────────

def search_node(state: ResearchState) -> Dict[str, Any]:
    """Search the web for each sub-query using DuckDuckGo."""
    all_results = []
    seen_urls = set()

    queries_to_search = [state["query"]] + state.get("sub_queries", [])

    for q in queries_to_search[:4]:   # limit API calls
        results = search_and_fetch(q, max_results=3)
        for r in results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                all_results.append(r)

    # Build deduplicated source list
    sources = [
        {"title": r["title"], "url": r["url"], "snippet": r["snippet"]}
        for r in all_results
        if r.get("url")
    ]

    return {
        "search_results": all_results,
        "sources": sources,
        "status": f"Searched web: {len(all_results)} sources found",
        "error": None,
    }


# ── Node 3: Index + FAISS Retrieval ─────────────────────────────────────────

def retrieve_node(state: ResearchState) -> Dict[str, Any]:
    """
    Chunk all search results, index in FAISS, then retrieve top-k
    chunks relevant to each sub-query.
    """
    search_results = state.get("search_results", [])

    if not search_results:
        return {
            "retrieved_chunks": [],
            "status": "No search results to index",
            "error": "Search returned no results",
        }

    # Build FAISS index
    vectorstore = build_vectorstore(search_results)

    # Retrieve for main query + sub-queries
    all_chunks = []
    seen = set()
    queries = [state["query"]] + state.get("sub_queries", [])

    for q in queries:
        hits = retrieve(vectorstore, q, k=4)
        for text, _meta in hits:
            if text not in seen:
                seen.add(text)
                all_chunks.append(text)

    return {
        "retrieved_chunks": all_chunks,
        "status": f"Indexed {len(search_results)} sources · Retrieved {len(all_chunks)} relevant chunks",
        "error": None,
    }


# ── Node 4: Synthesis ────────────────────────────────────────────────────────

def synthesize_node(state: ResearchState) -> Dict[str, Any]:
    """Synthesize retrieved chunks into dense research paragraphs."""
    chunks = state.get("retrieved_chunks", [])
    if not chunks:
        return {
            "draft_synthesis": "",
            "status": "Synthesis skipped — no chunks retrieved",
            "error": "No chunks to synthesize",
        }

    synthesis = generate_synthesis(
        query=state["query"],
        sub_queries=state.get("sub_queries", []),
        chunks=chunks,
    )

    return {
        "draft_synthesis": synthesis,
        "status": "Synthesis complete",
        "error": None,
    }


# ── Node 5: Report Generation ────────────────────────────────────────────────

def report_node(state: ResearchState) -> Dict[str, Any]:
    """Generate the final structured research report."""
    synthesis = state.get("draft_synthesis", "")
    if not synthesis:
        return {
            "final_report": "Could not generate report: synthesis is empty.",
            "status": "Report generation failed",
            "error": "Empty synthesis",
        }

    report = generate_report(
        query=state["query"],
        synthesis=synthesis,
        sources=state.get("sources", []),
    )

    return {
        "final_report": report,
        "iteration": state.get("iteration", 0) + 1,
        "status": "Report generated",
        "error": None,
    }


# ── Node 6: Quality Check (Conditional) ─────────────────────────────────────

def quality_check_node(state: ResearchState) -> Dict[str, Any]:
    """Check report quality and decide whether to refine."""
    max_iter = state.get("max_iterations", 2)
    current_iter = state.get("iteration", 1)

    if current_iter >= max_iter:
        return {"should_refine": False, "status": "Max iterations reached — finalizing"}

    is_good = check_quality(state["query"], state.get("final_report", ""))
    return {
        "should_refine": not is_good,
        "status": "Quality check passed" if is_good else "Quality check failed — refining",
    }


# ── Node 7: Refinement ───────────────────────────────────────────────────────

def refine_node(state: ResearchState) -> Dict[str, Any]:
    """
    Refinement pass: search for gaps and re-synthesize.
    Adds supplementary search using the research angle as a new query.
    """
    angle = state.get("research_angle", "")
    extra_query = f"{state['query']} {angle} detailed analysis"

    extra_results = search_and_fetch(extra_query, max_results=3)

    # Merge with existing
    existing = state.get("search_results", [])
    seen_urls = {r["url"] for r in existing}
    new_results = [r for r in extra_results if r["url"] not in seen_urls]

    all_results = existing + new_results
    all_sources = state.get("sources", []) + [
        {"title": r["title"], "url": r["url"], "snippet": r["snippet"]}
        for r in new_results
    ]

    return {
        "search_results": all_results,
        "sources": all_sources,
        "status": f"Refinement: added {len(new_results)} new sources",
        "error": None,
    }
