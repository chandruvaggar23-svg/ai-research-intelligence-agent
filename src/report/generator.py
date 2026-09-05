from typing import List, Dict
from src.llm.groq_client import chat


REPORT_SYSTEM = """You are an expert research analyst. Your task is to produce a well-structured, 
comprehensive research report based on synthesized information. 

Format rules:
- Use proper Markdown with headers (##, ###)
- Start with an Executive Summary (2–3 sentences)
- Use numbered sections for main findings
- Include bullet points for key facts within sections
- End with a Conclusion and Key Takeaways
- Be factual, objective, and cite information naturally ("According to sources...", "Research indicates...")
- Minimum 600 words, maximum 1200 words
- Do NOT use filler phrases like "Great question" or "Certainly"
"""


def generate_report(query: str, synthesis: str, sources: List[Dict[str, str]]) -> str:
    """
    Generate a structured research report from the synthesis.
    """
    sources_text = "\n".join(
        f"- [{s.get('title', 'Source')}]({s.get('url', '')})"
        for s in sources[:10]
        if s.get("url")
    )

    prompt = f"""Research Query: {query}

Synthesized Information:
{synthesis}

Available Sources:
{sources_text}

Generate a comprehensive, structured research report on the above topic. 
Include all major findings, analysis, and actionable insights.
End with a "## Sources" section listing the references."""

    return chat(REPORT_SYSTEM, prompt, temperature=0.2)


def generate_synthesis(query: str, sub_queries: List[str], chunks: List[str]) -> str:
    """
    First-pass synthesis from retrieved chunks.
    """
    system = """You are a research synthesis expert. Given retrieved text chunks from multiple sources,
synthesize the key information into coherent, dense paragraphs. Focus on:
- Main facts and findings
- Different perspectives or viewpoints
- Consensus and disagreements in the literature
- Key statistics, dates, or entities
Keep it dense and factual. No padding."""

    chunks_text = "\n\n---\n\n".join(chunks[:12])  # cap to avoid token limit

    prompt = f"""Main research question: {query}

Sub-questions being answered:
{chr(10).join(f"- {q}" for q in sub_queries)}

Retrieved content chunks:
{chunks_text}

Synthesize the above into comprehensive paragraphs covering all aspects of the research question."""

    return chat(system, prompt, temperature=0.1)


def plan_queries(query: str) -> Dict[str, object]:
    """
    Use LLM to decompose the main query into sub-queries and identify research angle.
    Returns dict with sub_queries (list) and research_angle (str).
    """
    system = """You are a research planning assistant. Break down a research query into 3–5 
specific sub-questions that together comprehensively answer the main query.
Also identify the key research angle (e.g., technical, historical, comparative, analytical).

Respond ONLY in this exact format (no extra text):
ANGLE: <one-line research angle>
SUB_QUERIES:
1. <sub-query 1>
2. <sub-query 2>
3. <sub-query 3>
4. <sub-query 4>
5. <sub-query 5>"""

    response = chat(system, f"Research query: {query}", temperature=0.3)

    lines = response.strip().splitlines()
    angle = ""
    sub_queries = []

    for line in lines:
        line = line.strip()
        if line.startswith("ANGLE:"):
            angle = line.replace("ANGLE:", "").strip()
        elif line and line[0].isdigit() and "." in line:
            q = line.split(".", 1)[-1].strip()
            if q:
                sub_queries.append(q)

    # Fallback if parsing failed
    if not sub_queries:
        sub_queries = [query]
    if not angle:
        angle = "General research"

    return {"sub_queries": sub_queries, "research_angle": angle}


def check_quality(query: str, report: str) -> bool:
    """
    Ask LLM if the report adequately answers the query. Returns True if good, False if needs refinement.
    """
    system = "You are a quality reviewer. Answer only YES or NO."
    prompt = f"""Does this report adequately answer the research query in sufficient depth?

Query: {query}

Report (first 800 chars): {report[:800]}

Answer YES if the report is comprehensive and directly answers the query. Answer NO if it's too vague, short, or misses key aspects."""

    response = chat(system, prompt, temperature=0.0)
    return "YES" in response.upper()
