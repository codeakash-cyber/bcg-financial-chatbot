"""
BCG X GenAI Job Simulation – AI-Powered Financial Chatbot
Author: Akash Kumar Sukla
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GFC Financial Chatbot | BCG X",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Dark professional theme */
.stApp {
    background: #0a0e1a;
    color: #e8edf5;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a2744 50%, #0d1b2a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.header-badge {
    display: inline-block;
    background: linear-gradient(90deg, #00d4aa, #0099ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.header-title {
    font-size: 28px;
    font-weight: 700;
    color: #e8edf5;
    margin: 0;
    letter-spacing: -0.5px;
}
.header-sub {
    color: #6b7fa3;
    font-size: 13px;
    margin-top: 6px;
    font-family: 'IBM Plex Mono', monospace;
}

/* Chat messages */
.chat-user {
    background: linear-gradient(135deg, #1a2744, #1e3a5f);
    border: 1px solid #2a4a7f;
    border-radius: 12px 12px 4px 12px;
    padding: 12px 16px;
    margin: 8px 0;
    color: #e8edf5;
    font-size: 14px;
    max-width: 75%;
    margin-left: auto;
}
.chat-bot {
    background: #111827;
    border: 1px solid #1e2d45;
    border-left: 3px solid #00d4aa;
    border-radius: 4px 12px 12px 12px;
    padding: 14px 16px;
    margin: 8px 0;
    color: #c8d8e8;
    font-size: 14px;
    font-family: 'IBM Plex Mono', monospace;
    max-width: 85%;
    line-height: 1.7;
}
.chat-bot-label {
    color: #00d4aa;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    margin-bottom: 6px;
    text-transform: uppercase;
}

/* Metric cards */
.metric-card {
    background: #111827;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
}
.metric-label {
    color: #6b7fa3;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
}
.metric-value {
    color: #00d4aa;
    font-size: 22px;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    margin-top: 4px;
}

/* Suggestion chips */
.chip-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 0;
}
.chip {
    background: #111827;
    border: 1px solid #2a4a7f;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: #7ab3e0;
    cursor: pointer;
    font-family: 'IBM Plex Mono', monospace;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1520;
    border-right: 1px solid #1e2d45;
}

/* Input */
.stTextInput input {
    background: #111827 !important;
    border: 1px solid #2a4a7f !important;
    border-radius: 8px !important;
    color: #e8edf5 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput input:focus {
    border-color: #00d4aa !important;
    box-shadow: 0 0 0 2px rgba(0,212,170,0.15) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #00d4aa, #0099ff) !important;
    color: #0a0e1a !important;
    font-weight: 700 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    border: none !important;
    border-radius: 8px !important;
    letter-spacing: 0.5px;
}
.stButton button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px);
}

/* Divider */
hr { border-color: #1e2d45 !important; }

/* Plotly charts background */
.js-plotly-plot { border-radius: 10px; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: #2a4a7f; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Financial Data ────────────────────────────────────────────────────────────
financial_data = {
    "Microsoft": {
        2023: {"revenue": 211.91, "net_income": 72.36,  "total_assets": 411.97,
               "total_liabilities": 205.75, "operating_cash_flow": 87.58},
        2024: {"revenue": 245.12, "net_income": 88.14,  "total_assets": 512.16,
               "total_liabilities": 243.69, "operating_cash_flow": 118.55},
        2025: {"revenue": 279.60, "net_income": 101.30, "total_assets": 526.00,
               "total_liabilities": 253.00, "operating_cash_flow": 135.00},
    },
    "Tesla": {
        2023: {"revenue": 96.77,  "net_income": 14.97,  "total_assets": 106.62,
               "total_liabilities": 43.11,  "operating_cash_flow": 13.26},
        2024: {"revenue": 97.69,  "net_income": 7.26,   "total_assets": 122.07,
               "total_liabilities": 48.39,  "operating_cash_flow": 14.92},
    },
    "Apple": {
        2023: {"revenue": 383.29, "net_income": 97.00,  "total_assets": 352.58,
               "total_liabilities": 290.44, "operating_cash_flow": 110.54},
        2024: {"revenue": 391.04, "net_income": 93.74,  "total_assets": 364.98,
               "total_liabilities": 308.03, "operating_cash_flow": 118.25},
    },
}

COMPANY_COLORS = {
    "Microsoft": "#00d4aa",
    "Tesla":     "#ff4d6d",
    "Apple":     "#7ab3e0",
}

SUPPORTED_COMPANIES = list(financial_data.keys())

# ── Chatbot Logic ─────────────────────────────────────────────────────────────
def detect_company(query):
    q = query.lower()
    for company in SUPPORTED_COMPANIES:
        if company.lower() in q:
            return company
    return None

def detect_year(query):
    for year in [2023, 2024, 2025]:
        if str(year) in query:
            return year
    return None

def latest_year(company):
    return max(financial_data[company].keys())

def yoy_change(company, metric):
    years = sorted(financial_data[company].keys())
    if len(years) < 2:
        return {}
    y1, y2 = years[-2], years[-1]
    v1 = financial_data[company][y1][metric]
    v2 = financial_data[company][y2][metric]
    pct = ((v2 - v1) / v1) * 100
    return {"from_year": y1, "to_year": y2, "from_val": v1, "to_val": v2, "pct": pct}

def get_revenue(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    year = detect_year(query) or latest_year(company)
    if year not in financial_data[company]:
        return f"No data for {company} FY{year}. Available: {list(financial_data[company].keys())}."
    rev = financial_data[company][year]["revenue"]
    return f"📈 {company}'s total revenue in FY{year} was **${rev:.2f}B**.\n\n💡 Try: 'How has {company}'s revenue changed?'"

def get_net_income(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    year = detect_year(query) or latest_year(company)
    if year not in financial_data[company]:
        return f"No data for {company} FY{year}."
    ni = financial_data[company][year]["net_income"]
    rev = financial_data[company][year]["revenue"]
    margin = (ni / rev) * 100
    return f"💰 {company}'s net income in FY{year} was **${ni:.2f}B** (profit margin: **{margin:.1f}%**).\n\n💡 Ask 'How has {company}'s net income changed?' to see the trend."

def get_net_income_change(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    ch = yoy_change(company, "net_income")
    if not ch:
        return f"Not enough data for {company}."
    direction = "📈 increased" if ch["pct"] > 0 else "📉 decreased"
    return (f"{company}'s net income {direction} from **${ch['from_val']:.2f}B** (FY{ch['from_year']}) "
            f"to **${ch['to_val']:.2f}B** (FY{ch['to_year']}), a change of **{ch['pct']:+.1f}%**.")

def get_revenue_change(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    ch = yoy_change(company, "revenue")
    if not ch:
        return f"Not enough data for {company}."
    direction = "📈 grew" if ch["pct"] > 0 else "📉 declined"
    return (f"{company}'s revenue {direction} from **${ch['from_val']:.2f}B** (FY{ch['from_year']}) "
            f"to **${ch['to_val']:.2f}B** (FY{ch['to_year']}), a change of **{ch['pct']:+.1f}%**.")

def get_cash_flow(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    year = detect_year(query) or latest_year(company)
    if year not in financial_data[company]:
        return f"No data for {company} FY{year}."
    ocf = financial_data[company][year]["operating_cash_flow"]
    return f"💵 {company}'s operating cash flow in FY{year} was **${ocf:.2f}B**.\n\n💡 Strong OCF signals a self-funding, healthy business."

def get_profit_margin(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    year = detect_year(query) or latest_year(company)
    if year not in financial_data[company]:
        return f"No data for {company} FY{year}."
    d = financial_data[company][year]
    margin = (d["net_income"] / d["revenue"]) * 100
    return f"📊 {company}'s net profit margin in FY{year} was **{margin:.1f}%** (net income ${d['net_income']:.2f}B on revenue ${d['revenue']:.2f}B)."

def get_financial_health(query):
    company = detect_company(query)
    if not company:
        return "Please specify a company — Microsoft, Tesla, or Apple."
    year = detect_year(query) or latest_year(company)
    if year not in financial_data[company]:
        return f"No data for {company} FY{year}."
    d = financial_data[company][year]
    equity = d["total_assets"] - d["total_liabilities"]
    debt_ratio = d["total_liabilities"] / d["total_assets"]
    margin = (d["net_income"] / d["revenue"]) * 100
    health = "🟢 Strong" if debt_ratio < 0.6 and margin > 15 else \
             "🟡 Moderate" if debt_ratio < 0.8 else "🔴 Leveraged"
    return (f"📊 **{company} Financial Health — FY{year}**\n\n"
            f"• Total Assets:         ${d['total_assets']:.2f}B\n"
            f"• Total Liabilities:    ${d['total_liabilities']:.2f}B\n"
            f"• Shareholders Equity:  ${equity:.2f}B\n"
            f"• Debt-to-Asset Ratio:  {debt_ratio:.2f}\n"
            f"• Net Profit Margin:    {margin:.1f}%\n"
            f"• Overall Assessment:   {health}")

def compare_revenue(query):
    lines = ["📈 **Revenue Comparison** (most recent fiscal year)\n"]
    for company in SUPPORTED_COMPANIES:
        year = latest_year(company)
        rev = financial_data[company][year]["revenue"]
        lines.append(f"• {company} (FY{year}): **${rev:.2f}B**")
    top = max(SUPPORTED_COMPANIES, key=lambda c: financial_data[c][latest_year(c)]["revenue"])
    lines.append(f"\n🏆 Highest revenue: **{top}**")
    return "\n".join(lines)

def compare_profit_margin(query):
    lines = ["💰 **Profit Margin Comparison** (most recent fiscal year)\n"]
    margins = {}
    for company in SUPPORTED_COMPANIES:
        year = latest_year(company)
        d = financial_data[company][year]
        m = (d["net_income"] / d["revenue"]) * 100
        margins[company] = m
        lines.append(f"• {company} (FY{year}): **{m:.1f}%**")
    top = max(margins, key=margins.get)
    lines.append(f"\n🏆 Highest margin: **{top}** ({margins[top]:.1f}%)")
    return "\n".join(lines)

def chatbot(user_query):
    q = user_query.lower().strip()

    if q in ("help", "?", "menu", "what can you do", "hi", "hello"):
        return ("👋 Hello! I'm the **GFC Financial Chatbot**, built during the BCG X GenAI Job Simulation.\n\n"
                "I can answer questions about **Microsoft**, **Tesla**, and **Apple**. Try:\n\n"
                "• *What is Microsoft's revenue in 2024?*\n"
                "• *How has Tesla's net income changed?*\n"
                "• *What is Apple's profit margin in 2023?*\n"
                "• *Compare revenue of all companies*\n"
                "• *What is Microsoft's financial health in 2024?*\n"
                "• *What is Tesla's cash flow?*")

    if any(w in q for w in ("compare", "all companies", "which company", "highest", "best")):
        if "margin" in q or "profit" in q:
            return compare_profit_margin(q)
        return compare_revenue(q)

    if "health" in q or ("assets" in q and "liabilities" in q):
        return get_financial_health(user_query)

    if "margin" in q or "profit margin" in q:
        return get_profit_margin(user_query)

    if "net income" in q or "earnings" in q or "profit" in q:
        if any(w in q for w in ("change", "trend", "over", "grew", "growth")):
            return get_net_income_change(user_query)
        return get_net_income(user_query)

    if "revenue" in q or "sales" in q or "turnover" in q:
        if any(w in q for w in ("change", "trend", "grew", "growth")):
            return get_revenue_change(user_query)
        return get_revenue(user_query)

    if "cash flow" in q or "operating cash" in q or "liquidity" in q:
        return get_cash_flow(user_query)

    return ("🤔 I didn't quite understand that. Type **help** to see what I can answer, or try:\n\n"
            "• *What is Apple's revenue in 2024?*\n"
            "• *Compare all companies*")

# ── Charts ────────────────────────────────────────────────────────────────────
def make_revenue_chart():
    fig = go.Figure()
    for company in SUPPORTED_COMPANIES:
        years = sorted(financial_data[company].keys())
        revenues = [financial_data[company][y]["revenue"] for y in years]
        fig.add_trace(go.Scatter(
            x=years, y=revenues, mode="lines+markers",
            name=company, line=dict(color=COMPANY_COLORS[company], width=2.5),
            marker=dict(size=8, color=COMPANY_COLORS[company]),
        ))
    fig.update_layout(
        title=dict(text="Revenue Trend (Billions USD)", font=dict(color="#e8edf5", size=13), x=0.02),
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(color="#6b7fa3", family="IBM Plex Mono"),
        xaxis=dict(gridcolor="#1e2d45", tickformat="d"),
        yaxis=dict(gridcolor="#1e2d45", tickprefix="$", ticksuffix="B"),
        legend=dict(bgcolor="#111827", bordercolor="#1e2d45"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=280,
    )
    return fig

def make_margin_chart():
    companies, margins = [], []
    for company in SUPPORTED_COMPANIES:
        year = latest_year(company)
        d = financial_data[company][year]
        m = (d["net_income"] / d["revenue"]) * 100
        companies.append(f"{company}\nFY{year}")
        margins.append(round(m, 1))
    fig = go.Figure(go.Bar(
        x=companies, y=margins,
        marker_color=[COMPANY_COLORS[c] for c in SUPPORTED_COMPANIES],
        text=[f"{m}%" for m in margins],
        textposition="outside", textfont=dict(color="#e8edf5", size=12),
    ))
    fig.update_layout(
        title=dict(text="Net Profit Margin (%)", font=dict(color="#e8edf5", size=13), x=0.02),
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(color="#6b7fa3", family="IBM Plex Mono"),
        xaxis=dict(gridcolor="#1e2d45"),
        yaxis=dict(gridcolor="#1e2d45", ticksuffix="%"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=280, showlegend=False,
    )
    return fig

def make_cashflow_chart():
    fig = go.Figure()
    for company in SUPPORTED_COMPANIES:
        years = sorted(financial_data[company].keys())
        ocf = [financial_data[company][y]["operating_cash_flow"] for y in years]
        fig.add_trace(go.Bar(
            x=[f"{company} FY{y}" for y in years], y=ocf,
            name=company, marker_color=COMPANY_COLORS[company], opacity=0.85,
        ))
    fig.update_layout(
        title=dict(text="Operating Cash Flow (Billions USD)", font=dict(color="#e8edf5", size=13), x=0.02),
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(color="#6b7fa3", family="IBM Plex Mono"),
        xaxis=dict(gridcolor="#1e2d45", tickangle=-30),
        yaxis=dict(gridcolor="#1e2d45", tickprefix="$", ticksuffix="B"),
        barmode="group", legend=dict(bgcolor="#111827", bordercolor="#1e2d45"),
        margin=dict(l=10, r=10, t=40, b=60),
        height=300,
    )
    return fig

# ── Session State ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": ("👋 Welcome! I'm the **GFC Financial Chatbot**, built as part of "
                                     "the BCG X GenAI Job Simulation on Forage.\n\n"
                                     "Ask me anything about **Microsoft**, **Tesla**, or **Apple** — "
                                     "revenue, net income, cash flow, profit margins, financial health, and more.\n\n"
                                     "Type **help** to see all supported queries.")}
    ]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 16px 0 8px 0;'>
        <div style='color:#00d4aa; font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:3px; text-transform:uppercase; margin-bottom:4px;'>BCG X · FORAGE</div>
        <div style='color:#e8edf5; font-size:16px; font-weight:700;'>GFC Financial<br>Chatbot</div>
        <div style='color:#6b7fa3; font-size:11px; margin-top:6px; font-family:"IBM Plex Mono",monospace;'>GenAI Job Simulation</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='color:#6b7fa3; font-size:11px; letter-spacing:2px; text-transform:uppercase; font-family:\"IBM Plex Mono\",monospace; margin-bottom:12px;'>Coverage</div>", unsafe_allow_html=True)

    for company in SUPPORTED_COMPANIES:
        years = sorted(financial_data[company].keys())
        st.markdown(f"""
        <div style='background:#111827; border:1px solid #1e2d45; border-left:3px solid {COMPANY_COLORS[company]}; border-radius:6px; padding:10px 12px; margin-bottom:8px;'>
            <div style='color:{COMPANY_COLORS[company]}; font-size:12px; font-weight:600;'>{company}</div>
            <div style='color:#6b7fa3; font-size:10px; font-family:"IBM Plex Mono",monospace;'>FY{years[0]}–FY{years[-1]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<div style='color:#6b7fa3; font-size:11px; letter-spacing:2px; text-transform:uppercase; font-family:\"IBM Plex Mono\",monospace; margin-bottom:12px;'>Quick Queries</div>", unsafe_allow_html=True)

    suggestions = [
        "What is Microsoft's revenue in 2024?",
        "How has Tesla's net income changed?",
        "What is Apple's profit margin?",
        "Compare revenue of all companies",
        "Microsoft financial health 2024",
        "What is Tesla's cash flow?",
        "Which company has the best margin?",
    ]
    for s in suggestions:
        if st.button(s, key=f"btn_{s}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": s})
            response = chatbot(s)
            st.session_state.messages.append({"role": "bot", "content": response})
            st.rerun()

    st.divider()
    st.markdown("""
    <div style='color:#6b7fa3; font-size:10px; font-family:"IBM Plex Mono",monospace; line-height:1.6;'>
    Data from SEC EDGAR 10-K filings.<br>Figures in billions USD.<br><br>
    Built by <span style='color:#00d4aa;'>Akash Kumar Sukla</span><br>
    BCG X GenAI Simulation · May 2026
    </div>
    """, unsafe_allow_html=True)

# ── Main Layout ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="header-badge">BCG X · GenAI Job Simulation · Forage</div>
    <div class="header-title">GFC Financial Intelligence Chatbot</div>
    <div class="header-sub">SEC 10-K Data · Microsoft · Tesla · Apple · FY2023–FY2025</div>
</div>
""", unsafe_allow_html=True)

# Top metrics
col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("Companies", "3"),
    ("Fiscal Years", "FY23–25"),
    ("Data Points", "35+"),
    ("Simulation", "BCG X"),
]
for col, (label, value) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs(["💬  Chat", "📊  Dashboard"])

with tab1:
    # Chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">🧑‍💼 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                content = msg["content"].replace("\n", "<br>").replace("**", "<b>").replace("</b><b>", "")
                # Simple bold fix
                import re
                content_raw = msg["content"]
                content_html = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color:#e8edf5">\1</strong>', content_raw)
                content_html = content_html.replace("\n", "<br>")
                st.markdown(f'<div class="chat-bot"><div class="chat-bot-label">▸ GFC Chatbot</div>{content_html}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Ask a question",
                placeholder="e.g. What is Microsoft's revenue in 2024?",
                label_visibility="collapsed"
            )
        with col_btn:
            submitted = st.form_submit_button("Send →")

        if submitted and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input.strip()})
            response = chatbot(user_input.strip())
            st.session_state.messages.append({"role": "bot", "content": response})
            st.rerun()

    # Clear chat
    if len(st.session_state.messages) > 1:
        if st.button("🗑 Clear Chat", use_container_width=False):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(make_revenue_chart(), use_container_width=True)
    with col_r:
        st.plotly_chart(make_margin_chart(), use_container_width=True)

    st.plotly_chart(make_cashflow_chart(), use_container_width=True)

    # Data table
    st.markdown("<div style='color:#6b7fa3; font-size:11px; letter-spacing:2px; text-transform:uppercase; font-family:\"IBM Plex Mono\",monospace; margin:16px 0 8px 0;'>Raw Data — All Companies</div>", unsafe_allow_html=True)
    rows = []
    for company in SUPPORTED_COMPANIES:
        for year, d in financial_data[company].items():
            equity = d["total_assets"] - d["total_liabilities"]
            margin = round((d["net_income"] / d["revenue"]) * 100, 1)
            rows.append({
                "Company": company, "FY": year,
                "Revenue ($B)": d["revenue"], "Net Income ($B)": d["net_income"],
                "Profit Margin (%)": margin,
                "Total Assets ($B)": d["total_assets"],
                "Shareholders Equity ($B)": round(equity, 2),
                "Op. Cash Flow ($B)": d["operating_cash_flow"],
            })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
