"""
LLM Émotions B2B — Interface Streamlit
Author: Martine Ouedraogo
"""

import os
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from prompts import SCENARIOS, EMOTIONS, FAMILIARITES, build_prompt
from llm_client import call_llm
from metrics import compute_metrics

# ─── CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Émotions B2B",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

/* ══ PALETTE (Linear / Vercel dark)
   bg:      #111827  gray-900
   surface: #1F2937  gray-800
   border:  #374151  gray-700
   muted:   #4B5563  gray-600
   body:    #9CA3AF  gray-400
   strong:  #D1D5DB  gray-300
   title:   #F9FAFB  gray-50
   accent:  #3B82F6  blue-500
══ */

.stApp { background: #111827 !important; }
.block-container { background: transparent !important; padding-top: 1.5rem !important; }

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {
    background: #0D1117 !important;
    border-right: 1px solid #374151 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #000000 !important; }
[data-testid="stSidebar"] .stCaption p { color: #9CA3AF !important; }
[data-testid="stSidebar"] [role="option"] { color: #000000 !important; background: #FFFFFF !important; }
[data-testid="stSidebar"] [role="listbox"] { background: #FFFFFF !important; }
[data-testid="stSidebar"] label { color: #D1D5DB !important; }
[data-testid="stSidebar"] .stRadio label p { color: #D1D5DB !important; }

/* Logo sidebar */
.sb-mark {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #3B82F6, #6366F1);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; margin-bottom: 0.75rem;
}
.sb-name { font-size: 0.92rem; font-weight: 700; color: #F9FAFB !important; margin: 0; }
.sb-ver  { font-size: 0.72rem; color: #6B7280 !important; margin: 0.15rem 0 0; }
.sb-label {
    display: block; font-size: 0.62rem; font-weight: 700;
    color: #4B5563 !important; text-transform: uppercase;
    letter-spacing: 0.13em; margin: 1.5rem 0 0.45rem;
}

/* ══ HEADER ══ */
.ph-wrap {
    background: #1F2937;
    border: 1px solid #374151;
    border-radius: 14px;
    padding: 2rem 2.25rem 1.75rem;
    margin-bottom: 1.75rem;
    position: relative; overflow: hidden;
}
.ph-wrap::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #3B82F6, #6366F1, #8B5CF6);
}
.ph-label {
    font-size: 0.67rem; font-weight: 700; color: #60A5FA;
    text-transform: uppercase; letter-spacing: 0.14em; margin: 0 0 0.5rem;
}
.ph-title {
    font-size: 1.9rem; font-weight: 800; color: #F9FAFB;
    letter-spacing: -0.03em; line-height: 1.15; margin: 0 0 0.5rem;
}
.ph-desc { font-size: 0.9rem; color: #9CA3AF; line-height: 1.65; margin: 0; max-width: 620px; }

/* ══ TABS ══ */
.stTabs [data-baseweb="tab-list"] {
    background: #1F2937 !important;
    border: 1px solid #374151 !important;
    border-radius: 10px 10px 0 0 !important;
    gap: 0 !important; padding: 0.3rem 0.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #6B7280 !important;
    font-size: 0.875rem !important; font-weight: 500 !important;
    padding: 0.6rem 1.2rem !important; border-radius: 7px !important;
    border: none !important; margin: 0.1rem !important;
    transition: all 0.15s !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #D1D5DB !important; background: rgba(255,255,255,0.05) !important;
}
.stTabs [aria-selected="true"] {
    background: #111827 !important; color: #F9FAFB !important; font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding: 0 !important; }

/* ══ BOUTONS ══ */
.stButton > button {
    background: #2563EB !important; color: #FFFFFF !important;
    border: none !important; padding: 0.65rem 1.6rem !important;
    border-radius: 8px !important; font-size: 0.875rem !important;
    font-weight: 600 !important; letter-spacing: 0.01em !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4) !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #1D4ED8 !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.45) !important;
}

/* ══ CARTES ══ */
.card {
    background: #1F2937; border: 1px solid #374151;
    border-radius: 12px; padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3); margin-bottom: 1rem;
}
.card-blue {
    background: #1F2937; border: 1px solid #374151;
    border-top: 3px solid #3B82F6; border-radius: 12px;
    padding: 1.5rem; box-shadow: 0 1px 4px rgba(0,0,0,0.3); margin-bottom: 1rem;
}

/* ══ SECTION LABEL ══ */
.sec-lbl {
    font-size: 0.65rem; font-weight: 700; color: #4B5563;
    text-transform: uppercase; letter-spacing: 0.14em;
    margin: 0 0 0.85rem; display: block;
}

/* ══ TAGS ══ */
.tag {
    display: inline-flex; align-items: center;
    padding: 0.25rem 0.7rem; border-radius: 6px;
    font-size: 0.77rem; font-weight: 500;
    margin-right: 0.35rem; margin-bottom: 0.35rem;
}
.tag-blue   { background: rgba(59,130,246,0.12); color: #93C5FD; border: 1px solid rgba(59,130,246,0.25); }
.tag-purple { background: rgba(99,102,241,0.12); color: #A5B4FC; border: 1px solid rgba(99,102,241,0.25); }
.tag-green  { background: rgba(16,185,129,0.10); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.22); }
.tag-amber  { background: rgba(245,158,11,0.10); color: #FCD34D; border: 1px solid rgba(245,158,11,0.22); }
.tag-gray   { background: rgba(75,85,99,0.25);   color: #9CA3AF; border: 1px solid #374151; }
.tag-red    { background: rgba(239,68,68,0.10);  color: #FCA5A5; border: 1px solid rgba(239,68,68,0.22); }

/* ══ SCENARIO CARD ══ */
.sc-row { display: flex; align-items: flex-start; gap: 1rem; }
.sc-icon {
    width: 48px; height: 48px; flex-shrink: 0;
    background: #374151; border: 1px solid #4B5563;
    border-radius: 12px; display: flex;
    align-items: center; justify-content: center; font-size: 1.4rem;
}
.sc-title { font-size: 1rem; font-weight: 700; color: #F9FAFB; margin: 0 0 0.2rem; }
.sc-meta  { font-size: 0.78rem; color: #6B7280; margin: 0; }
.sc-text-box {
    background: #111827; border: 1px solid #374151;
    border-radius: 8px; padding: 0.9rem 1rem; margin-top: 1rem;
}
.sc-text-box p { font-size: 0.855rem !important; color: #9CA3AF !important; line-height: 1.75 !important; margin: 0 !important; }
.sc-text-lbl { font-size: 0.62rem; font-weight: 700; color: #4B5563; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.35rem; }

/* ══ PARAMÈTRES ROW ══ */
.params-row { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0 1.25rem; }
.params-lbl { font-size: 0.72rem; font-weight: 600; color: #6B7280; margin-right: 0.25rem; }

/* ══ RÉPONSE ══ */
.resp-wrap {
    background: #1F2937; border: 1px solid #374151;
    border-left: 3px solid #3B82F6;
    border-radius: 0 12px 12px 0;
    padding: 1.75rem 2rem; margin: 1.5rem 0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
}
.resp-pill {
    display: inline-block; background: rgba(59,130,246,0.12);
    color: #93C5FD; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    padding: 0.2rem 0.65rem; border-radius: 20px;
    border: 1px solid rgba(59,130,246,0.25); margin-bottom: 1rem;
}
.resp-text { font-size: 0.92rem; color: #D1D5DB; line-height: 1.9; white-space: pre-wrap; margin: 0; }

/* ══ METRIC CARDS ══ */
.m-card {
    background: #1F2937; border: 1px solid #374151;
    border-radius: 10px; padding: 1.1rem 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.m-val { font-size: 2rem; font-weight: 800; color: #F9FAFB; line-height: 1; margin-bottom: 0.2rem; }
.m-lbl { font-size: 0.7rem; font-weight: 600; color: #4B5563; text-transform: uppercase; letter-spacing: 0.08em; }
.m-bar-bg { margin-top: 0.7rem; height: 4px; border-radius: 2px; background: #374151; overflow: hidden; }
.m-bar-fill { height: 100%; border-radius: 2px; }
.status-on  { display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.25rem 0.6rem; border-radius: 5px; font-size: 0.75rem; font-weight: 600; background: rgba(16,185,129,0.10); color: #6EE7B7; border: 1px solid rgba(16,185,129,0.22); margin-top: 0.4rem; }
.status-off { display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.25rem 0.6rem; border-radius: 5px; font-size: 0.75rem; font-weight: 600; background: rgba(75,85,99,0.2); color: #6B7280; border: 1px solid #374151; margin-top: 0.4rem; }

/* ══ COMPARISON ══ */
.cmp-card {
    background: #1F2937; border: 1px solid #374151;
    border-radius: 12px; padding: 1.2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    margin-bottom: 0.75rem; height: 100%;
}
.cmp-head { border-bottom: 1px solid #374151; padding-bottom: 0.65rem; margin-bottom: 0.65rem; }
.cmp-combo { font-size: 0.875rem; font-weight: 700; color: #F9FAFB; margin: 0 0 0.2rem; }
.cmp-stats { font-size: 0.75rem; color: #6B7280; margin: 0; }
.cmp-text  { font-size: 0.81rem; color: #9CA3AF; line-height: 1.7; margin: 0; }

/* ══ METHODOLOGIE ══ */
.m-block {
    background: #1F2937; border: 1px solid #374151;
    border-radius: 12px; padding: 1.4rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2); height: 100%;
}
.m-num {
    width: 32px; height: 32px; border-radius: 8px;
    background: #374151; border: 1px solid #4B5563;
    color: #9CA3AF; font-size: 0.78rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 0.85rem;
}
.m-block h4 { font-size: 0.9rem !important; font-weight: 700 !important; color: #F9FAFB !important; margin: 0 0 0.4rem !important; }
.m-block p  { font-size: 0.81rem !important; color: #6B7280 !important; line-height: 1.65 !important; margin: 0 !important; }

/* ══ ABOUT STATS ══ */
.stat-box {
    background: #1F2937; border: 1px solid #374151;
    border-radius: 12px; padding: 1.5rem 1rem; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.stat-num  { font-size: 2.5rem; font-weight: 800; color: #60A5FA; line-height: 1; margin-bottom: 0.3rem; }
.stat-desc { font-size: 0.72rem; font-weight: 600; color: #4B5563; text-transform: uppercase; letter-spacing: 0.07em; }

/* ══ INFO BAR ══ */
.info-bar {
    background: #1F2937; border: 1px solid #374151; border-left: 3px solid #3B82F6;
    border-radius: 0 10px 10px 0;
    padding: 0.9rem 1.2rem; display: flex; align-items: flex-start;
    gap: 0.7rem; margin-bottom: 1.5rem;
}
.info-bar p { font-size: 0.84rem !important; color: #9CA3AF !important; margin: 0 !important; line-height: 1.6 !important; }
.info-bar p b { color: #D1D5DB !important; }

/* ══ LIEN BUTTONS ══ */
.link-btn {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.65rem 0.9rem; background: #1F2937;
    border: 1px solid #374151; border-radius: 8px;
    font-size: 0.83rem; color: #9CA3AF !important;
    text-decoration: none !important; margin-bottom: 0.5rem;
    transition: all 0.15s;
}
.link-btn:hover { border-color: #60A5FA !important; color: #F9FAFB !important; }

/* ══ CONSTRAINT LIST ══ */
.constraint-item { display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 0.85rem; }
.constraint-dot { width: 6px; height: 6px; border-radius: 50%; background: #3B82F6; margin-top: 0.5rem; flex-shrink: 0; }
.constraint-title { font-size: 0.84rem; font-weight: 600; color: #D1D5DB; margin: 0 0 0.15rem; }
.constraint-desc  { font-size: 0.78rem; color: #6B7280; margin: 0; line-height: 1.5; }

/* ══ OVERRIDES STREAMLIT ══ */
h1, h2, h3, h4 { color: #F9FAFB !important; }
p, li { color: #9CA3AF !important; }
.stMarkdown p { color: #9CA3AF !important; }
label, [data-testid="stWidgetLabel"] p { color: #D1D5DB !important; }
code { background: #111827 !important; color: #93C5FD !important; border-radius: 4px !important; padding: 0.15em 0.4em !important; border: 1px solid #374151 !important; }
pre { background: #0D1117 !important; border: 1px solid #374151 !important; border-radius: 10px !important; }
[data-testid="stAlert"] { background: #1F2937 !important; border: 1px solid #374151 !important; border-left: 3px solid #3B82F6 !important; border-radius: 0 10px 10px 0 !important; color: #9CA3AF !important; }
[data-testid="stMetricValue"] { color: #60A5FA !important; }
[data-testid="stMetricLabel"] { color: #6B7280 !important; }
.stDataFrame { border: 1px solid #374151 !important; border-radius: 10px !important; }
a { color: #60A5FA !important; }
hr { border-color: #374151 !important; }
[data-testid="stDownloadButton"] > button { background: #1F2937 !important; color: #9CA3AF !important; border: 1px solid #374151 !important; box-shadow: none !important; }
[data-testid="stDownloadButton"] > button:hover { border-color: #60A5FA !important; color: #F9FAFB !important; }
footer, #MainMenu { visibility: hidden; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #111827; }
::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #4B5563; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1.25rem; border-bottom: 1px solid #374151; margin-bottom: 0.5rem;">
        <div class="sb-mark">⚡</div>
        <p class="sb-name">LLM Émotions B2B</p>
        <p class="sb-ver">Prototype de recherche · v1.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sb-label">Mode de génération</span>', unsafe_allow_html=True)
    mode = st.radio(
        "mode",
        options=["mock", "openai"],
        format_func=lambda x: {"mock": "Mock  (sans API)", "openai": "OpenAI  (réel)"}[x],
        label_visibility="collapsed",
    )
    if mode == "openai":
        if bool(os.getenv("OPENAI_API_KEY")):
            st.success("Clé API détectée")
        else:
            st.warning("OPENAI_API_KEY manquante")

    st.markdown('<span class="sb-label">Scénario B2B</span>', unsafe_allow_html=True)
    scenario_id = st.selectbox(
        "sc",
        options=list(SCENARIOS.keys()),
        format_func=lambda k: f"{SCENARIOS[k]['icone']}  {SCENARIOS[k]['titre']}",
        label_visibility="collapsed",
    )

    st.markdown('<span class="sb-label">Registre émotionnel</span>', unsafe_allow_html=True)
    emotion_id = st.selectbox(
        "emo",
        options=list(EMOTIONS.keys()),
        format_func=lambda k: f"{EMOTIONS[k]['icone']}  {EMOTIONS[k]['label']}",
        label_visibility="collapsed",
    )
    st.caption(EMOTIONS[emotion_id]["description"])

    st.markdown('<span class="sb-label">Niveau de familiarité</span>', unsafe_allow_html=True)
    familiarite_id = st.selectbox(
        "fam",
        options=list(FAMILIARITES.keys()),
        format_func=lambda k: f"{FAMILIARITES[k]['icone']}  {FAMILIARITES[k]['label']}",
        label_visibility="collapsed",
    )
    st.caption(FAMILIARITES[familiarite_id]["description"])

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <p style="font-size:0.73rem; color:#9CA3AF !important; line-height:1.7; margin:0;">
        M1 Informatique · Univ. Lumière Lyon 2<br>
        <a href="https://www.linkedin.com/in/marte-oued" style="color:#60A5FA !important;">Martine Ouedraogo</a> ·
        <a href="https://portfoliomarte.vercel.app" style="color:#60A5FA !important;">Portfolio</a>
    </p>
    """, unsafe_allow_html=True)

# ─── PAGE HEADER ──────────────────────────────────────────────────────
st.markdown("""
<div class="ph-wrap">
    <p class="ph-label">Recherche NLP appliqué · Université Lumière Lyon 2</p>
    <h1 class="ph-title">LLM Émotions B2B</h1>
    <p class="ph-desc">
        Étude des variations linguistiques contrôlées d'un LLM sur des scénarios d'échec
        en relation client — paramètres : registre émotionnel × niveau de familiarité.
    </p>
    <div style="margin-top:1rem; display:flex; flex-wrap:wrap; gap:0.4rem;">
        <span class="tag tag-blue">Python 3.10</span>
        <span class="tag tag-purple">OpenAI API</span>
        <span class="tag tag-green">Streamlit</span>
        <span class="tag tag-amber">Prompt Engineering</span>
        <span class="tag tag-gray">NLP · Métriques</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-bar">
    <span style="font-size:1.1rem; flex-shrink:0;">💡</span>
    <p><b>Note méthodologique :</b> L'IA n'éprouve pas d'émotions.
    Cette étude analyse exclusivement des <b>variations linguistiques paramétriques</b>
    et leur impact mesurable sur la structure des réponses générées.</p>
</div>
""", unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Génération  ",
    "  Comparaison  ",
    "  Méthodologie  ",
    "  À propos  ",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — GÉNÉRATION
# ══════════════════════════════════════════════════════════════════════
with tab1:
    scenario = SCENARIOS[scenario_id]
    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    # Scénario
    st.markdown(f"""
    <div class="card-blue">
        <div class="sc-row">
            <div class="sc-icon">{scenario['icone']}</div>
            <div>
                <p class="sc-title">{scenario['titre']}</p>
                <p class="sc-meta">{scenario['contexte']} &nbsp;·&nbsp; Émotion client : {scenario['emotion_probable_client']}</p>
            </div>
        </div>
        <div class="sc-text-box">
            <p class="sc-text-lbl">Scénario neutre (input)</p>
            <p>{scenario['texte_neutre']}</p>
        </div>
        <div style="margin-top:0.9rem; display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
            <span style="font-size:0.72rem; font-weight:600; color:#94A3B8;">Enjeu client :</span>
            <span style="font-size:0.84rem; color:#475569;">{scenario['enjeu_client']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Paramètres actifs
    st.markdown(f"""
    <div class="params-row">
        <span class="params-lbl">Paramètres actifs</span>
        <span class="tag tag-blue">{EMOTIONS[emotion_id]['icone']} {EMOTIONS[emotion_id]['label']}</span>
        <span class="tag tag-purple">{FAMILIARITES[familiarite_id]['icone']} {FAMILIARITES[familiarite_id]['label']}</span>
        <span class="tag tag-gray">⚙ {mode.upper()}</span>
    </div>
    """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        generate = st.button("Générer la réponse →", use_container_width=True, key="btn_gen")

    if generate:
        with st.spinner("Génération en cours…"):
            result = call_llm(scenario_id, emotion_id, familiarite_id, mode=mode)

        if result["error"]:
            st.warning(f"Mode {result['mode']} utilisé — {result['error']}")

        # Réponse
        st.markdown(f"""
        <div class="resp-wrap">
            <span class="resp-pill">Réponse · {result['mode'].upper()}</span>
            <p class="resp-text">{result['response']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Métriques
        metrics = compute_metrics(result["response"])

        st.markdown('<span class="sec-lbl" style="margin-top:1.75rem; display:block;">Métriques calculées</span>', unsafe_allow_html=True)

        def pct(val, max_val):
            return min(int(val / max_val * 100), 100)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            p = pct(metrics["nb_mots"], 400)
            st.markdown(f"""<div class="m-card">
                <div class="m-val">{metrics['nb_mots']}</div>
                <div class="m-lbl">Mots</div>
                <div class="m-bar-bg"><div class="m-bar-fill" style="width:{p}%; background:linear-gradient(90deg,#3B82F6,#6366F1);"></div></div>
            </div>""", unsafe_allow_html=True)

        with c2:
            p = pct(metrics["nb_marqueurs_reconnaissance"], 6)
            st.markdown(f"""<div class="m-card">
                <div class="m-val">{metrics['nb_marqueurs_reconnaissance']}</div>
                <div class="m-lbl">Reconnaissance</div>
                <div class="m-bar-bg"><div class="m-bar-fill" style="width:{p}%; background:linear-gradient(90deg,#0EA5E9,#3B82F6);"></div></div>
            </div>""", unsafe_allow_html=True)

        with c3:
            p = pct(metrics["nb_marqueurs_action"], 6)
            st.markdown(f"""<div class="m-card">
                <div class="m-val">{metrics['nb_marqueurs_action']}</div>
                <div class="m-lbl">Action</div>
                <div class="m-bar-bg"><div class="m-bar-fill" style="width:{p}%; background:linear-gradient(90deg,#10B981,#0EA5E9);"></div></div>
            </div>""", unsafe_allow_html=True)

        with c4:
            p = pct(metrics["nb_marqueurs_formalite"], 5)
            st.markdown(f"""<div class="m-card">
                <div class="m-val">{metrics['nb_marqueurs_formalite']}</div>
                <div class="m-lbl">Formalité</div>
                <div class="m-bar-bg"><div class="m-bar-fill" style="width:{p}%; background:linear-gradient(90deg,#8B5CF6,#6366F1);"></div></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        c5, c6, _, __ = st.columns(4)
        with c5:
            cls = "status-on" if metrics["vouvoiement"] else "status-off"
            lbl = "Détecté" if metrics["vouvoiement"] else "Absent"
            st.markdown(f"""<div class="m-card">
                <div class="m-lbl">Vouvoiement</div>
                <span class="{cls}">{'●' if metrics['vouvoiement'] else '○'} {lbl}</span>
            </div>""", unsafe_allow_html=True)
        with c6:
            cls = "status-on" if metrics["tutoiement"] else "status-off"
            lbl = "Détecté" if metrics["tutoiement"] else "Absent"
            st.markdown(f"""<div class="m-card">
                <div class="m-lbl">Tutoiement</div>
                <span class="{cls}">{'●' if metrics['tutoiement'] else '○'} {lbl}</span>
            </div>""", unsafe_allow_html=True)

        # Historique
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({
            "timestamp": datetime.now().isoformat(),
            "scenario_id": scenario_id,
            "emotion_id": emotion_id,
            "familiarite_id": familiarite_id,
            "mode": result["mode"],
            "response": result["response"],
            **metrics,
        })

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        df_export = pd.DataFrame(st.session_state.history)
        st.download_button(
            "Télécharger l'historique (CSV)",
            data=df_export.to_csv(index=False).encode("utf-8"),
            file_name=f"llm_b2b_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — COMPARAISON
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        scenario_cmp = st.selectbox(
            "Scénario à comparer",
            options=list(SCENARIOS.keys()),
            format_func=lambda k: f"{SCENARIOS[k]['icone']}  {SCENARIOS[k]['titre']}",
            key="cmp_sc",
        )
    with c2:
        nb_var = st.slider("Nombre de variations", 2, 6, 4)

    col_run, _ = st.columns([1, 3])
    with col_run:
        run_cmp = st.button("Lancer la comparaison →", key="btn_cmp", use_container_width=True)

    if run_cmp:
        combos = [(e, f) for e in EMOTIONS.keys() for f in FAMILIARITES.keys()][:nb_var]
        results = []
        with st.spinner("Génération des variations…"):
            for emo, fam in combos:
                res = call_llm(scenario_cmp, emo, fam, mode=mode)
                m = compute_metrics(res["response"])
                results.append({
                    "emotion": EMOTIONS[emo]["label"],
                    "emotion_icone": EMOTIONS[emo]["icone"],
                    "familiarite": FAMILIARITES[fam]["label"],
                    "fam_icone": FAMILIARITES[fam]["icone"],
                    "response": res["response"],
                    **m,
                })

        st.markdown('<span class="sec-lbl" style="margin-top:1.5rem; display:block;">Résultats par combinaison</span>', unsafe_allow_html=True)
        for i in range(0, len(results), 2):
            pair = results[i:i+2]
            cols = st.columns(len(pair))
            for col, r in zip(cols, pair):
                with col:
                    vou = "Vouv." if r["vouvoiement"] else "Tutoi."
                    st.markdown(f"""
                    <div class="cmp-card">
                        <div class="cmp-head">
                            <p class="cmp-combo">{r['emotion_icone']} {r['emotion']} &nbsp;·&nbsp; {r['fam_icone']} {r['familiarite']}</p>
                            <p class="cmp-stats">{r['nb_mots']} mots &nbsp;·&nbsp; {r['nb_marqueurs_reconnaissance']} reco &nbsp;·&nbsp; {r['nb_marqueurs_action']} action &nbsp;·&nbsp; {vou}</p>
                        </div>
                        <p class="cmp-text">{r['response'][:300]}…</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Radar chart
        st.markdown('<span class="sec-lbl" style="margin-top:2rem; display:block;">Analyse radar — comparaison des métriques</span>', unsafe_allow_html=True)

        categories = ["Mots (×0.1)", "Reconnaissance", "Action", "Formalité", "Vouvoiement"]
        palette   = ["#3B82F6", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444", "#EC4899"]
        palette_f = ["rgba(59,130,246,0.12)", "rgba(139,92,246,0.12)", "rgba(16,185,129,0.12)",
                     "rgba(245,158,11,0.12)", "rgba(239,68,68,0.12)", "rgba(236,72,153,0.12)"]

        fig = go.Figure()
        for idx, r in enumerate(results):
            vals = [
                round(r["nb_mots"] * 0.1, 1),
                r["nb_marqueurs_reconnaissance"],
                r["nb_marqueurs_action"],
                r["nb_marqueurs_formalite"],
                1 if r["vouvoiement"] else 0,
            ]
            vals_c = vals + [vals[0]]
            cats_c = categories + [categories[0]]
            fig.add_trace(go.Scatterpolar(
                r=vals_c, theta=cats_c,
                fill="toself",
                fillcolor=palette_f[idx % len(palette_f)],
                line=dict(color=palette[idx % len(palette)], width=2),
                name=f"{r['emotion_icone']} {r['emotion'][:10]} / {r['fam_icone']} {r['familiarite'][:10]}",
                hovertemplate="%{theta}: %{r}<extra></extra>",
            ))

        fig.update_layout(
            polar=dict(
                bgcolor="#1F2937",
                radialaxis=dict(
                    visible=True, gridcolor="#374151",
                    tickfont=dict(color="#6B7280", size=10),
                    linecolor="#374151",
                ),
                angularaxis=dict(
                    tickfont=dict(color="#9CA3AF", size=11),
                    linecolor="#374151", gridcolor="#2D3748",
                ),
            ),
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(family="Inter, sans-serif", color="#9CA3AF"),
            legend=dict(
                font=dict(size=11, color="#9CA3AF"),
                bgcolor="rgba(31,41,55,0.95)",
                bordercolor="#374151", borderwidth=1,
            ),
            height=420,
            margin=dict(t=30, b=30, l=60, r=60),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tableau
        st.markdown('<span class="sec-lbl" style="margin-top:1.25rem; display:block;">Tableau récapitulatif</span>', unsafe_allow_html=True)
        df_cmp = pd.DataFrame([{
            "Émotion": r["emotion"],
            "Familiarité": r["familiarite"],
            "Mots": r["nb_mots"],
            "Reconnaissance": r["nb_marqueurs_reconnaissance"],
            "Action": r["nb_marqueurs_action"],
            "Formalité": r["nb_marqueurs_formalite"],
            "Vouvoiement": "✓" if r["vouvoiement"] else "—",
        } for r in results])
        st.dataframe(df_cmp, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — MÉTHODOLOGIE
# ══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
    st.markdown('<span class="sec-lbl">Architecture en 4 blocs</span>', unsafe_allow_html=True)

    cols = st.columns(4)
    blocks = [
        ("01", "Scénarios B2B",
         "5 cas d'échec réels formulés de façon neutre et factuelle — aucun mot émotionnel dans l'input."),
        ("02", "Paramètres linguistiques",
         "4 registres émotionnels × 3 niveaux de familiarité = 12 combinaisons contrôlées."),
        ("03", "Méta-prompt",
         "Template paramétrable injectant scénario + émotion + familiarité avec contraintes éthiques explicites."),
        ("04", "Génération & métriques",
         "Appel LLM, calcul de 6 métriques exploratoires, export CSV. Mode mock sans clé API."),
    ]
    for col, (num, title, desc) in zip(cols, blocks):
        with col:
            st.markdown(f"""
            <div class="m-block">
                <div class="m-num">{num}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.75rem'></div>", unsafe_allow_html=True)

    col_eth, col_prompt = st.columns([1, 2])

    with col_eth:
        st.markdown('<span class="sec-lbl">Contraintes éthiques</span>', unsafe_allow_html=True)
        constraints = [
            ("Respectueux", "Ton professionnel maintenu en toutes circonstances."),
            ("Transparent", "L'incident est reconnu sans être minimisé ni noyé."),
            ("Non-manipulatoire", "Aucune stratégie émotionnelle de détournement."),
            ("Orienté action", "Plan concret : étapes, délais, contact nommé."),
            ("Intègre", "Les précisions manquantes sont explicitement demandées."),
        ]
        for title, desc in constraints:
            st.markdown(f"""
            <div class="constraint-item">
                <div class="constraint-dot"></div>
                <div>
                    <p class="constraint-title">{title}</p>
                    <p class="constraint-desc">{desc}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_prompt:
        st.markdown('<span class="sec-lbl">Méta-prompt généré (paramètres actifs)</span>', unsafe_allow_html=True)
        st.code(build_prompt(scenario_id, emotion_id, familiarite_id), language="markdown")

# ══════════════════════════════════════════════════════════════════════
# TAB 4 — À PROPOS
# ══════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

    # Stats row
    st.markdown('<span class="sec-lbl">Chiffres clés</span>', unsafe_allow_html=True)
    for col, (num, label) in zip(st.columns(5), [
        ("5", "Scénarios B2B"),
        ("4", "Registres émotionnels"),
        ("3", "Niveaux de familiarité"),
        ("60", "Combinaisons possibles"),
        ("6", "Métriques calculées"),
    ]):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-num">{num}</div>
                <div class="stat-desc">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
    col_why, col_stack = st.columns([3, 2])

    with col_why:
        st.markdown('<span class="sec-lbl">Objectif du projet</span>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
            <p style="font-size:0.9rem !important; color:#94A3B8 !important; line-height:1.8 !important; margin:0 0 1.2rem !important;">
                Ce prototype académique explore comment des <strong style="color:#E2E8F0;">paramètres linguistiques explicites</strong>
                — registre émotionnel et niveau de familiarité — modifient structurellement les réponses
                d'un LLM dans des contextes B2B à fort enjeu relationnel.
            </p>
            <div style="display:flex; flex-direction:column; gap:0.7rem;">
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <div style="width:28px; height:28px; background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:0.75rem; flex-shrink:0; color:#93C5FD; font-weight:700;">→</div>
                    <p style="font-size:0.84rem !important; color:#94A3B8 !important; margin:0 !important;">Comprendre comment <strong style="color:#E2E8F0;">piloter</strong> la sortie d'un LLM via des paramètres contrôlés</p>
                </div>
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <div style="width:28px; height:28px; background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:0.75rem; flex-shrink:0; color:#93C5FD; font-weight:700;">→</div>
                    <p style="font-size:0.84rem !important; color:#94A3B8 !important; margin:0 !important;">Mesurer l'<strong style="color:#E2E8F0;">impact quantifiable</strong> de chaque paramètre sur la structure de la réponse</p>
                </div>
                <div style="display:flex; align-items:center; gap:0.75rem;">
                    <div style="width:28px; height:28px; background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); border-radius:7px; display:flex; align-items:center; justify-content:center; font-size:0.75rem; flex-shrink:0; color:#93C5FD; font-weight:700;">→</div>
                    <p style="font-size:0.84rem !important; color:#94A3B8 !important; margin:0 !important;">Garantir que les variations restent <strong style="color:#E2E8F0;">éthiques et professionnelles</strong> en toutes circonstances</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_stack:
        st.markdown('<span class="sec-lbl">Stack technique</span>', unsafe_allow_html=True)
        stack = [
            ("Interface",    "Streamlit",            "tag-green"),
            ("LLM",          "OpenAI gpt-4o-mini",   "tag-purple"),
            ("Données",      "Pandas · Plotly",       "tag-blue"),
            ("Mock",         "Génération paramétrique","tag-amber"),
            ("Langage",      "Python 3.10+",          "tag-gray"),
        ]
        rows = "".join([
            f"""<div style="display:flex; justify-content:space-between; align-items:center;
                padding: 0.6rem 0; border-bottom:1px solid #1E2D45;">
                <span style="font-size:0.82rem; color:#64748B;">{lbl}</span>
                <span class="tag {cls}" style="margin:0;">{val}</span>
            </div>""" for lbl, val, cls in stack
        ])
        st.markdown(f'<div class="card">{rows}</div>', unsafe_allow_html=True)

        st.markdown('<span class="sec-lbl" style="margin-top:1.25rem; display:block;">Liens</span>', unsafe_allow_html=True)
        st.markdown("""
        <a href="https://github.com/MarteOued/llm-emotions-b2b-prototype" class="link-btn">
            <span>⌥</span> GitHub — code source
        </a>
        <a href="https://portfoliomarte.vercel.app" class="link-btn">
            <span>◈</span> Portfolio
        </a>
        <a href="https://www.linkedin.com/in/marte-oued" class="link-btn">
            <span>◉</span> LinkedIn
        </a>
        """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:2.5rem 0 1.5rem; border-top:1px solid #1E2D45; margin-top:3rem;">
    <p style="font-size:0.78rem !important; color:#334155 !important; margin:0 !important;">
        Martine Ouedraogo &nbsp;·&nbsp; Master 1 Informatique &nbsp;·&nbsp; Université Lumière Lyon 2 &nbsp;·&nbsp; 2026
    </p>
</div>
""", unsafe_allow_html=True)
