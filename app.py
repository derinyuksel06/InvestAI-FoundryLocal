import streamlit as st

from src.query import (
    ask_investai,
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="InvestAI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    :root {
        --teal: #0f766e;
        --border: rgba(100,116,139,0.22);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(15,118,110,0.08),
                transparent 32%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(37,99,235,0.05),
                transparent 28%
            );
    }

    .block-container {
        max-width: 1080px;
        padding-top: 2.4rem;
        padding-bottom: 7rem;
    }

    .brand-kicker {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        opacity: 0.58;
        margin-bottom: 0.7rem;
    }

    .hero-title {
        font-size: 4rem;
        line-height: 0.95;
        font-weight: 850;
        letter-spacing: -0.055em;
        margin-bottom: 0.85rem;
    }

    .hero-title span {
        color: #0f766e;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.75;
        opacity: 0.74;
        max-width: 780px;
        margin-bottom: 1.6rem;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-bottom: 1.7rem;
    }

    .pill {
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.48rem 0.8rem;
        font-size: 0.82rem;
    }

    .info-card {
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.15rem 1.2rem;
        margin-bottom: 1.5rem;
    }

    .source-card {
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.65rem 0.8rem;
        margin-top: 0.4rem;
        font-size: 0.84rem;
        background: rgba(15,118,110,0.045);
    }

    .tiny-label {
        font-size: 0.7rem;
        opacity: 0.54;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        font-weight: 700;
    }

    .metric-card {
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        height: 100%;
    }

    .metric-number {
        font-size: 1.25rem;
        font-weight: 800;
    }

    .metric-label {
        font-size: 0.76rem;
        opacity: 0.58;
    }

    [data-testid="stSidebar"] {
        border-right:
            1px solid
            rgba(100,116,139,0.18);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## InvestAI"
    )

    st.caption(
        "Local investment education, "
        "grounded in trusted sources."
    )

    st.divider()

    st.markdown(
        "### Knowledge Base"
    )

    st.markdown(
        """
**Investing Basics**  
Stocks, bonds, returns and risk.

**ETFs**  
Fund structure and diversification.

**Diversification**  
Managing concentration risk.

**Financial Statements**  
Balance sheet, income statement and cash flow.

**10-K Reports**  
Business, Risk Factors and MD&A.

**Bonds**  
Debt securities and corporate bonds.

**Fees & Expenses**  
Fund costs and expense ratios.

**Compound Interest**  
Long-term compounding concepts.
"""
    )

    st.divider()

    st.markdown(
        "### Runtime"
    )

    st.success(
        "Foundry Local active"
    )

    st.caption(
        "Local Qwen model"
    )

    st.caption(
        "Semantic retrieval enabled"
    )

    st.caption(
        "Similarity safeguard enabled"
    )

    st.caption(
        "Advice & prediction guardrail enabled"
    )

    st.divider()

    st.warning(
        "Educational use only. "
        "InvestAI does not provide "
        "personalised financial advice."
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="brand-kicker">
SOURCE-GROUNDED LOCAL AI
</div>

<div class="hero-title">
Learn investing with
<span>InvestAI</span>
</div>

<div class="hero-subtitle">
A private investment education assistant that retrieves
information from trusted local sources before generating an
answer with Microsoft Foundry Local.
</div>

<div class="pill-row">
<span class="pill">🔒 Private & local</span>
<span class="pill">📚 Trusted knowledge base</span>
<span class="pill">🔎 Semantic retrieval</span>
<span class="pill">🛡️ Safety guardrails</span>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(
    4
)


with m1:

    st.markdown(
        """
<div class="metric-card">
<div class="metric-number">Local</div>
<div class="metric-label">AI inference</div>
</div>
""",
        unsafe_allow_html=True,
    )


with m2:

    st.markdown(
        """
<div class="metric-card">
<div class="metric-number">9</div>
<div class="metric-label">Source documents</div>
</div>
""",
        unsafe_allow_html=True,
    )


with m3:

    st.markdown(
        """
<div class="metric-card">
<div class="metric-number">Top-3</div>
<div class="metric-label">Semantic retrieval</div>
</div>
""",
        unsafe_allow_html=True,
    )


with m4:

    st.markdown(
        """
<div class="metric-card">
<div class="metric-number">0.30</div>
<div class="metric-label">Similarity threshold</div>
</div>
""",
        unsafe_allow_html=True,
    )


st.markdown(
    "<br>",
    unsafe_allow_html=True,
)


# ============================================================
# HOW IT WORKS
# ============================================================

st.markdown(
    """
<div class="info-card">

<div class="tiny-label">
HOW INVESTAI WORKS
</div>

<br>

1. Your question passes through a safety guardrail.<br>
2. The question is converted into an embedding.<br>
3. InvestAI retrieves the most relevant trusted passages.<br>
4. Relevant context is sent to the local Foundry model.<br>
5. Low-confidence or personalised-advice questions are refused.

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.markdown(
    "### Explore the knowledge base"
)


col1, col2, col3 = st.columns(
    3
)


with col1:

    q1 = st.button(
        "What is a bond?",
        use_container_width=True
    )


with col2:

    q2 = st.button(
        "How do fund fees affect returns?",
        use_container_width=True
    )


with col3:

    q3 = st.button(
        "What is compound interest?",
        use_container_width=True
    )


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


if "pending_question" not in st.session_state:

    st.session_state.pending_question = None


if q1:

    st.session_state.pending_question = (
        "What is a bond?"
    )


if q2:

    st.session_state.pending_question = (
        "How do investment fund fees "
        "affect returns?"
    )


if q3:

    st.session_state.pending_question = (
        "What is compound interest?"
    )


# ============================================================
# HISTORY
# ============================================================

st.divider()

st.markdown(
    "### Ask InvestAI"
)


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get(
            "sources"
        ):

            st.markdown(
                """
<div class="tiny-label">
Sources
</div>
""",
                unsafe_allow_html=True,
            )

            for source in message[
                "sources"
            ]:

                st.markdown(
                    f"""
<div class="source-card">
📄 {source}
</div>
""",
                    unsafe_allow_html=True,
                )


# ============================================================
# INPUT
# ============================================================

typed_question = st.chat_input(
    "Ask about investing, ETFs, bonds, fees, "
    "diversification, financial statements, or 10-K reports..."
)


question = None


if typed_question:

    question = typed_question


elif st.session_state.pending_question:

    question = (
        st.session_state
        .pending_question
    )

    st.session_state.pending_question = None


# ============================================================
# ANSWER
# ============================================================

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )


    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching trusted sources "
            "and generating a local answer..."
        ):

            result = ask_investai(
                question
            )


        answer = result[
            "answer"
        ]

        sources = result[
            "sources"
        ]


        st.markdown(
            answer
        )


        if sources:

            st.markdown(
                """
<div class="tiny-label">
Sources
</div>
""",
                unsafe_allow_html=True,
            )


            for source in sources:

                st.markdown(
                    f"""
<div class="source-card">
📄 {source}
</div>
""",
                    unsafe_allow_html=True,
                )


        elif result[
            "refused"
        ]:

            st.caption(
                "InvestAI safely declined this question."
            )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )