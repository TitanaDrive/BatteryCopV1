
import streamlit as st
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="SP-VERT Scalability Checker", page_icon="🔋", layout="centered")

# Title
st.markdown("""
    <style>
    .title { font-size: 36px; font-weight: bold; }
    .verdict { font-size: 24px; font-weight: bold; margin-top: 20px; }
    .tag { font-size: 18px; color: #888; }
    .highlight { background-color: #f5f5f5; padding: 10px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔍 SP-VERT: Battery Scalability Checker</div>', unsafe_allow_html=True)
st.markdown("**Science Police Verdict Engine v1** — *because battery dreams need reality checks.*")

# Chemistry database with styling and resource context
chemistry_data = {
    "NaFM | HC": {"Wh/kg": 134, "kg/kWh": 7.46, "resource_flag": "🟢 SCALABLE"},
    "NaNM | HC": {"Wh/kg": 134, "kg/kWh": 7.46, "resource_flag": "🟢 SCALABLE"},
    "NaFM | Sn": {"Wh/kg": 185, "kg/kWh": 5.4, "resource_flag": "🟡 LIMITED — Tin bottleneck"},
    "NFPP | HC": {"Wh/kg": 111, "kg/kWh": 9.01, "resource_flag": "🟢 SCALABLE"},
    "LFP | Graphite": {"Wh/kg": 160, "kg/kWh": 6.25, "resource_flag": "🟢 SCALABLE"},
    "NMC | Graphite": {"Wh/kg": 250, "kg/kWh": 4.0, "resource_flag": "🔴 CONSTRAINED — Ni/Co supply"},
    "NMC | Si": {"Wh/kg": 300, "kg/kWh": 3.33, "resource_flag": "🟡 AGGRESSIVE — Ni/Si tradeoffs"},
    "NaNM | Anode-Free": {"Wh/kg": 207, "kg/kWh": 4.8, "resource_flag": "🟡 LIMITED — Anode-free challenge"},
}

# User inputs
st.markdown("### Chemistry & Claim Input")
selected_chem = st.selectbox("Choose chemistry pair", list(chemistry_data.keys()))
roadmap_year = st.slider("Select roadmap year", 2024, 2040, 2025)
claim = st.number_input("Enter claimed Wh/kg (optional)", value=0)

# Fetch chemistry baseline and compute roadmap boost
base = chemistry_data[selected_chem]
improved_whkg = base["Wh/kg"] + (roadmap_year - 2025) * 2
claimed = claim if claim > 0 else improved_whkg
kg_kwh = base["kg/kWh"]
scalability = base["resource_flag"]

# Verdict logic
if claim > 0:
    if claim <= improved_whkg * 1.1:
        verdict = "✅ REALISTIC — Your claim is grounded in physical possibility."
    elif claim <= improved_whkg * 1.3:
        verdict = "⚠️ AGGRESSIVE — You’re stretching into high-ambition territory."
    else:
        verdict = "🚨 HYPE ALERT — Your claim exceeds known limits."
else:
    verdict = "📊 Model Preview — No claim provided."

# Output display
st.markdown("---")
st.markdown(f"### Selected Chemistry: `{selected_chem}`")
st.markdown('<div class="highlight">', unsafe_allow_html=True)
st.markdown(f"- **Projected Wh/kg (by {roadmap_year})**: `{improved_whkg:.1f}`")
st.markdown(f"- **Mass per kWh (kg)**: `{kg_kwh:.2f}`")
st.markdown(f"- **Scalability Status**: `{scalability}`")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("---")
st.markdown(f'<div class="verdict">{verdict}</div>', unsafe_allow_html=True)
