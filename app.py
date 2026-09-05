import os
import time
import threading
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchIQ",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #070B14;
    --panel: #0D1322;
    --panel-2: #111A2E;
    --border: rgba(148,163,184,.14);
    --border-strong: rgba(99,102,241,.35);
    --text: #F8FAFC;
    --muted: #94A3B8;
    --muted-2: #64748B;
    --blue: #4F7CFF;
    --violet: #8B5CF6;
    --cyan: #22D3EE;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(79,124,255,.12), transparent 28%),
        radial-gradient(circle at 90% 8%, rgba(139,92,246,.10), transparent 25%),
        #070B14 !important;
    color: var(--text);
}

.main .block-container {
    padding: 2.2rem 2.5rem 4rem;
    max-width: 1180px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B101C 0%, #080C15 100%) !important;
    border-right: 1px solid rgba(148,163,184,.10) !important;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: var(--muted);
}

section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stTextInput label {
    color: #CBD5E1 !important;
    font-weight: 600 !important;
}

/* Main typography */
h1, h2, h3, h4 {
    color: #F8FAFC !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.035em !important;
}

h1 {
    font-size: 2.15rem !important;
    line-height: 1.1 !important;
}

p, li {
    color: #94A3B8;
}

/* Text inputs */
.stTextArea textarea,
.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(13,19,34,.88) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(148,163,184,.16) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.025) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextArea textarea {
    padding: 15px 16px !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #64748B !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: rgba(99,102,241,.75) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.12) !important;
}

/* Buttons */
.stButton > button {
    min-height: 46px !important;
    background: linear-gradient(135deg, #4F7CFF 0%, #7C5CFF 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,.10) !important;
    border-radius: 11px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    letter-spacing: .01em !important;
    box-shadow: 0 8px 25px rgba(79,124,255,.18) !important;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}

.stButton > button *,
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

.stButton > button:hover {
    filter: brightness(1.08) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 12px 32px rgba(79,124,255,.28) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Example query buttons */
div[data-testid="column"] .stButton > button {
    min-height: 96px !important;
    background: linear-gradient(145deg, rgba(17,26,46,.96), rgba(13,19,34,.96)) !important;
    border: 1px solid rgba(148,163,184,.13) !important;
    box-shadow: none !important;
    color: #CBD5E1 !important;
    padding: 12px !important;
}

div[data-testid="column"] .stButton > button:hover {
    border-color: rgba(99,102,241,.48) !important;
    background: linear-gradient(145deg, rgba(24,35,62,1), rgba(15,23,42,1)) !important;
    box-shadow: 0 10px 28px rgba(0,0,0,.22) !important;
}

/* Download button */
.stDownloadButton > button {
    background: rgba(79,124,255,.08) !important;
    color: #AFC1FF !important;
    border: 1px solid rgba(79,124,255,.28) !important;
    box-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: rgba(79,124,255,.14) !important;
}

/* Cards */
.research-card,
.stat-card,
.source-item,
.report-container {
    background: linear-gradient(145deg, rgba(13,19,34,.92), rgba(10,15,27,.92)) !important;
    border: 1px solid rgba(148,163,184,.13) !important;
    box-shadow: 0 16px 45px rgba(0,0,0,.18) !important;
    backdrop-filter: blur(14px);
}

.research-card {
    border-radius: 16px !important;
    padding: 1.35rem 1.5rem !important;
}

.stat-card {
    border-radius: 14px !important;
    padding: 1.05rem !important;
}

.stat-card:hover {
    border-color: rgba(99,102,241,.30) !important;
}

.stat-val {
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    color: #F8FAFC !important;
}

.stat-label {
    font-size: .72rem !important;
    color: #64748B !important;
    margin-top: 4px !important;
    text-transform: uppercase;
    letter-spacing: .08em;
}

/* Step indicator */
.step-row {
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 10px 0 !important;
    border-bottom: 1px solid rgba(148,163,184,.08) !important;
    font-size: 13px;
}

.step-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 12px currentColor;
}

.dot-done { background: #22C55E !important; }
.dot-active { background: #F59E0B !important; }
.dot-wait { background: #334155 !important; box-shadow: none; }

/* Source cards */
.source-item {
    border-radius: 11px !important;
    padding: 12px 14px !important;
    margin-bottom: 8px !important;
}

.source-title {
    font-size: 13px;
    font-weight: 650;
    color: #E2E8F0;
}

.source-url {
    font-size: 11px;
    color: #60A5FA;
}

.source-snippet {
    font-size: 12px;
    color: #64748B;
    margin-top: 5px;
    line-height: 1.5;
}

/* Report */
.report-container {
    border-radius: 16px !important;
    padding: 2rem !important;
    color: #CBD5E1 !important;
    line-height: 1.75 !important;
}

.report-container h1,
.report-container h2,
.report-container h3 {
    color: #F8FAFC !important;
}

.report-container strong {
    color: #E2E8F0 !important;
}

/* Pills */
.sq-pill {
    display: inline-block;
    background: rgba(99,102,241,.09);
    border: 1px solid rgba(99,102,241,.22);
    color: #A5B4FC;
    border-radius: 999px;
    padding: 5px 11px;
    font-size: 11px;
    margin: 3px;
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #4F7CFF, #8B5CF6) !important;
    border-radius: 99px !important;
}

.stProgress > div {
    background: rgba(148,163,184,.10) !important;
    border-radius: 99px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 5px;
    background: rgba(13,19,34,.72);
    border: 1px solid rgba(148,163,184,.10);
    padding: 5px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    height: 38px;
    border-radius: 8px;
    color: #64748B;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,.14) !important;
    color: #C7D2FE !important;
}

/* Expanders / alerts */
.streamlit-expanderHeader {
    background: rgba(13,19,34,.78) !important;
    border: 1px solid rgba(148,163,184,.12) !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
}

.stAlert {
    background: rgba(79,124,255,.08) !important;
    border: 1px solid rgba(79,124,255,.20) !important;
    border-radius: 11px !important;
}

/* Selectbox dropdown */
div[data-baseweb="popover"] {
    background: #0D1322 !important;
    border: 1px solid rgba(148,163,184,.15) !important;
}

div[data-baseweb="menu"] {
    background: #0D1322 !important;
}

div[data-baseweb="menu"] * {
    color: #CBD5E1 !important;
}

/* Divider */
hr {
    border-color: rgba(148,163,184,.10) !important;
}

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] {
    background: transparent !important;
}

/* Responsive */
@media (max-width: 900px) {
    .main .block-container {
        padding: 1.25rem 1rem 3rem;
    }
    h1 {
        font-size: 1.75rem !important;
    }
}

/* ===== ResearchIQ Premium v2 ===== */
.hero-wrap {
    position: relative;
    overflow: hidden;
    padding: 2.6rem 2.7rem 2.35rem;
    margin: .25rem 0 2rem;
    border-radius: 22px;
    background:
        radial-gradient(circle at 85% 15%, rgba(124,92,255,.20), transparent 27%),
        radial-gradient(circle at 15% 80%, rgba(34,211,238,.08), transparent 28%),
        linear-gradient(145deg, rgba(17,26,46,.98), rgba(9,14,26,.98));
    border: 1px solid rgba(148,163,184,.14);
    box-shadow: 0 24px 70px rgba(0,0,0,.30);
}

.hero-wrap:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -80px;
    bottom: -120px;
    border-radius: 50%;
    border: 1px solid rgba(99,102,241,.18);
    box-shadow: 0 0 0 25px rgba(99,102,241,.025), 0 0 0 55px rgba(99,102,241,.018);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(99,102,241,.10);
    border: 1px solid rgba(99,102,241,.25);
    color: #A5B4FC;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .12em;
}

.hero-title {
    margin: 18px 0 10px !important;
    font-size: 3.25rem !important;
    line-height: 1.02 !important;
    font-weight: 800 !important;
    letter-spacing: -.055em !important;
}

.hero-title span {
    background: linear-gradient(100deg, #60A5FA, #8B5CF6 55%, #22D3EE);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    max-width: 690px;
    margin: 0 !important;
    color: #94A3B8 !important;
    font-size: 14px !important;
    line-height: 1.7 !important;
}

.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 19px;
}

.hero-chips span {
    padding: 6px 10px;
    border-radius: 8px;
    color: #CBD5E1;
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(148,163,184,.10);
    font-size: 10px;
    font-weight: 600;
}

.section-label {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 0 0 12px;
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .09em;
}

.section-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 23px;
    height: 23px;
    border-radius: 7px;
    color: #A5B4FC;
    background: rgba(99,102,241,.10);
    border: 1px solid rgba(99,102,241,.22);
    font-size: 9px;
}

.query-hint {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: -5px 0 13px;
    color: #64748B;
    font-size: 11px;
}

.query-hint span:first-child {
    color: #F59E0B;
}

[data-testid="stTextArea"] textarea {
    min-height: 125px !important;
}

[data-testid="stTextArea"] > div > div {
    background: rgba(13,19,34,.92) !important;
    border-radius: 14px !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(99,102,241,.75) !important;
}

/* Make the four example cards feel like selectable tools */
div[data-testid="column"] .stButton > button {
    min-height: 52px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    border-radius: 11px !important;
    font-size: 11px !important;
}

/* Main CTA gets a stronger visual hierarchy */
div[data-testid="stHorizontalBlock"] .stButton > button {
    letter-spacing: .015em !important;
}

@media (max-width: 700px) {
    .hero-wrap {
        padding: 2rem 1.35rem;
        border-radius: 17px;
    }
    .hero-title {
        font-size: 2.35rem !important;
    }
    .hero-chips {
        gap: 5px;
    }
}


.run-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 15px 17px;
    margin-bottom: 14px;
    border: 1px solid rgba(99,102,241,.18);
    border-radius: 13px;
    background: rgba(99,102,241,.055);
}
.run-pulse {
    color: #8B5CF6;
    font-size: 14px;
    text-shadow: 0 0 14px #8B5CF6;
}
.run-title {
    color: #E2E8F0;
    font-size: 13px;
    font-weight: 750;
}
.run-subtitle {
    color: #64748B;
    font-size: 10px;
    margin-top: 2px;
}

</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:4px 0 16px;border-bottom:1px solid #1E2D4A;margin-bottom:16px">
        <div style="width:32px;height:32px;border-radius:8px;background:#2563EB;display:flex;align-items:center;justify-content:center;font-size:16px">🔬</div>
        <div>
            <div style="font-weight:800;font-size:15px;color:#F1F5F9">ResearchIQ</div>
            <div style="font-size:11px;color:#64748B">AI Research Agent</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Settings**")

    max_results = st.slider("Search results per query", 2, 8, 4)
    max_iter = st.selectbox("Refinement iterations", [1, 2, 3], index=1)
    model = st.selectbox("AI model", [
    "openai/gpt-oss-120b",
])
    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px;color:#64748B;line-height:1.6">
    <strong style="color:#94A3B8">Pipeline</strong><br/>
    🔍 DuckDuckGo search<br/>
    🗄️ FAISS vector retrieval<br/>
    🤖 Groq LLaMA synthesis<br/>
    📝 LangGraph orchestration
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    api_key = st.text_input("Groq API Key", type="password",
                             value=os.getenv("GROQ_API_KEY", ""),
                             placeholder="gsk_...")
    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

    st.markdown("""
    <div style="font-size:11px;color:#475569;margin-top:8px">
    Get a free key at <a href="https://console.groq.com" style="color:#2563EB">console.groq.com</a>
    </div>
    """, unsafe_allow_html=True)


# ── Main UI ───────────────────────────────────────────────────────────────────

# Premium hero
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">✦ AI-POWERED RESEARCH WORKSPACE</div>
    <h1 class="hero-title">Research Intelligence<br/><span>Agent</span></h1>
    <p class="hero-subtitle">
        Turn complex questions into evidence-backed research reports.
        Search, retrieve, reason, and synthesize — in one workspace.
    </p>
    <div class="hero-chips">
        <span>⚡ Groq LLaMA</span>
        <span>🧠 FAISS Retrieval</span>
        <span>🔗 LangGraph</span>
        <span>🌐 Web Research</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Query workspace
st.markdown("""
<div class="section-label">
    <span class="section-number">01</span>
    <span>Research workspace</span>
</div>
""", unsafe_allow_html=True)

examples = [
    ("⚛️", "Quantum Computing", "What are the latest advances in quantum computing?"),
    ("🧠", "LLM Architecture", "Compare transformer vs state space models for LLMs"),
    ("🧬", "CRISPR", "How does CRISPR gene editing work and what are its applications?"),
    ("🚗", "Autonomous Vehicles", "What is the current state of autonomous vehicles?"),
]

cols = st.columns(4)
for i, (icon, title, ex) in enumerate(examples):
    with cols[i]:
        if st.button(f"{icon}  {title}", key=f"ex_{i}", use_container_width=True):
            st.session_state["query_input"] = ex
            st.rerun()

query = st.text_area(
    "Research query",
    value=st.session_state.get("query_input", ""),
    placeholder="Ask a complex question… e.g. What are the economic impacts of AI automation on the global workforce?",
    height=125,
    key="query_box",
    label_visibility="collapsed",
)

st.markdown("""
<div class="query-hint">
    <span>💡</span>
    <span>Tip: Be specific about the topic, comparison, timeframe, or outcome you want researched.</span>
</div>
""", unsafe_allow_html=True)

col_btn, col_clear = st.columns([3, 1])
with col_btn:
    run = st.button("✦  Run Deep Research", use_container_width=True)
with col_clear:
    if st.button("↺  Clear", use_container_width=True):
        for k in ["result", "query_input", "query_box"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── Run Pipeline ──────────────────────────────────────────────────────────────
if run and query.strip():
    if not os.getenv("GROQ_API_KEY"):
        st.error("⚠️ Add your Groq API key in the sidebar to run the agent.")
    else:
        os.environ["MAX_SEARCH_RESULTS"] = str(max_results)
        os.environ["GROQ_MODEL"] = model

        # Lazy import to avoid slow startup
        from src.agent.graph import run_research

        st.markdown("---")
        st.markdown("""<div class="run-header"><span class="run-pulse">●</span><div><div class="run-title">Deep research in progress</div><div class="run-subtitle">Your agent is planning, searching, retrieving and synthesizing evidence.</div></div></div>""", unsafe_allow_html=True)

        steps = [
            ("plan",          "Planning sub-queries"),
            ("search",        "Searching the web"),
            ("retrieve",      "Indexing with FAISS & retrieving"),
            ("synthesize",    "Synthesizing with Groq LLaMA"),
            ("report",        "Generating report"),
            ("quality_check", "Quality check"),
        ]

        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        steps_placeholder = st.empty()

        # Render step indicators
        def render_steps(done_count: int, current: int):
            html = '<div class="research-card">'
            for i, (_, label) in enumerate(steps):
                if i < done_count:
                    dot = 'dot-done'
                    icon = '✓'
                    color = '#2563EB'
                elif i == current:
                    dot = 'dot-active'
                    icon = '⟳'
                    color = '#F59E0B'
                else:
                    dot = 'dot-wait'
                    icon = '·'
                    color = '#1C2A4A'
                html += f'<div class="step-row"><div class="step-dot {dot}"></div><span style="color:{color}">{icon} {label}</span></div>'
            html += '</div>'
            return html

        # Animate step progress
        for i, (step_id, label) in enumerate(steps):
            progress_bar.progress(int((i / len(steps)) * 100))
            status_placeholder.markdown(f"<p style='color:#F59E0B;font-size:13px'>⟳ {label}…</p>", unsafe_allow_html=True)
            steps_placeholder.markdown(render_steps(i, i), unsafe_allow_html=True)
            time.sleep(0.2)

        try:
            result = run_research(query.strip(), max_iterations=max_iter)
            st.session_state["result"] = result

            progress_bar.progress(100)
            status_placeholder.markdown("<p style='color:#2563EB;font-size:13px'>✓ Research complete!</p>", unsafe_allow_html=True)
            steps_placeholder.markdown(render_steps(len(steps), -1), unsafe_allow_html=True)

        except Exception as e:
            progress_bar.empty()
            status_placeholder.empty()
            steps_placeholder.empty()
            st.error(f"Agent error: {e}")
            st.stop()


# ── Display Results ───────────────────────────────────────────────────────────
if "result" in st.session_state:
    result = st.session_state["result"]
    st.markdown("---")

    # Stats row
    sources = result.get("sources", [])
    chunks = result.get("retrieved_chunks", [])
    sub_qs = result.get("sub_queries", [])
    iters = result.get("iteration", 1)

    s1, s2, s3, s4 = st.columns(4)
    for col, val, label in [
        (s1, len(sources), "Sources found"),
        (s2, len(chunks), "Chunks retrieved"),
        (s3, len(sub_qs), "Sub-queries"),
        (s4, iters, "Iterations"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val">{val}</div>
                <div class="stat-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Sub-queries
    if sub_qs:
        pills = "".join(f'<span class="sq-pill">↳ {q}</span>' for q in sub_qs)
        st.markdown(f"""
        <div class="research-card">
            <p style="font-size:11px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">Research Plan</p>
            <div><span style="font-size:13px;color:#94A3B8;font-weight:500">{result.get('research_angle','')}</span></div>
            <div style="margin-top:8px">{pills}</div>
        </div>
        """, unsafe_allow_html=True)

    # Report
    report = result.get("final_report", "")
    if report:
        tab_report, tab_sources, tab_raw = st.tabs(["📄 Report", "🔗 Sources", "🗂️ Raw Data"])

        with tab_report:
            st.markdown(f"""
            <div class="report-container">
            """, unsafe_allow_html=True)
            st.markdown(report)
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                "⬇️ Download Report (Markdown)",
                data=report,
                file_name=f"research_{query[:40].replace(' ','_')}.md",
                mime="text/markdown",
            )

        with tab_sources:
            if sources:
                for i, s in enumerate(sources, 1):
                    st.markdown(f"""
                    <div class="source-item">
                        <div class="source-title">{i}. {s.get('title','Untitled')}</div>
                        <div class="source-url">{s.get('url','')}</div>
                        <div class="source-snippet">{s.get('snippet','')[:180]}…</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No sources found.")

        with tab_raw:
            with st.expander("Retrieved chunks (FAISS output)"):
                for i, chunk in enumerate(chunks, 1):
                    st.markdown(f"**Chunk {i}**")
                    st.text(chunk[:400])
                    st.markdown("---")

            with st.expander("Full agent state"):
                safe_state = {k: v for k, v in result.items() if k != "retrieved_chunks"}
                st.json(safe_state)

    else:
        st.warning("The agent completed but produced no report. Check your API key and try again.")

elif not run:
    # Landing state
    st.markdown("""
    <div class="research-card" style="border-style:dashed;text-align:center;padding:2.5rem">
        <div style="font-size:2.5rem;margin-bottom:12px">🔬</div>
        <div style="font-weight:700;font-size:1rem;color:#E2E8F0;margin-bottom:6px">Ask anything. Get a structured research report.</div>
        <div style="font-size:13px;color:#64748B;max-width:480px;margin:0 auto;line-height:1.6">
        The agent plans sub-queries, searches the web with DuckDuckGo, indexes sources using FAISS,
        and synthesizes a comprehensive report using Groq LLaMA — all in one click.
        </div>
    </div>
    """, unsafe_allow_html=True)