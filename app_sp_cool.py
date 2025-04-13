
import streamlit as st
import pandas as pd

st.set_page_config(page_title="SP-VERT by Science Police", page_icon="🚓", layout="centered")

# Title with style
st.markdown("""
    <style>
    .sp-header {
        font-size: 42px;
        font-weight: bold;
        color: #FFFFFF;
        background-color: #1E1E1E;
        padding: 15px 25px;
        border-radius: 10px;
        text-align: center;
    }
    .box {
        background-color: #F4F4F4;
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .verdict-box {
        font-size: 24px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="sp-header">⚡ SP-VERT — Battery Scalability Verificator</div>', unsafe_allow_html=True)
st.markdown("### Built by Science Police — because reality deserves a badge.")

# Chemistry baseline data
chemistry_data = {
    "NaFM | HC": {"Wh/kg": 134, "kg/kWh": 7.46, "resource_flag": "🟢 SCALABLE"},
    "NaNM | HC": {"Wh/kg": 134, "kg/kWh": 7.46, "resource_flag": "🟢 SCALABLE"},
    "NaFM | Sn": {"Wh/kg": 185, "kg/kWh": 5.4, "resource_flag": "🟡 LIMITED – Tin bottleneck"},
    "NFPP | HC": {"Wh/kg": 111, "kg/kWh": 9.01, "resource_flag": "🟢 SCALABLE"},
    "LFP | Graphite": {"Wh/kg": 160, "kg/kWh": 6.25, "resource_flag": "🟢 SCALABLE"},
    "NMC | Graphite": {"Wh/kg": 250, "kg/kWh": 4.0, "resource_flag": "🔴 CONSTRAINED – Ni/Co"},
    "NMC | Si": {"Wh/kg": 300, "kg/kWh": 3.33, "resource_flag": "🟡 AGGRESSIVE – Ni/Si limits"},
    "NaNM | Anode-Free": {"Wh/kg": 207, "kg/kWh": 4.8, "resource_flag": "🟡 Emerging – Anode-free challenge"},
}

# Input section
st.markdown("#### Select your combo and claim")
selected_chem = st.selectbox("Choose battery chemistry", list(chemistry_data.keys()))
year = st.slider("Roadmap year", 2024, 2040, 2025)
claim = st.number_input("Claimed Wh/kg (leave blank for default model)", value=0)

# Pull chemistry data
chem = chemistry_data[selected_chem]
boosted = chem["Wh/kg"] + (year - 2025) * 2
used_value = claim if claim > 0 else boosted
kgpkwh = chem["kg/kWh"]
scalability = chem["resource_flag"]

# Verdict logic
if claim > 0:
    if claim <= boosted * 1.1:
        verdict = "✅ REALISTIC — Based on current trends and roadmap."
        color = "#28a745"
    elif claim <= boosted * 1.3:
        verdict = "⚠️ AGGRESSIVE — Borderline believable, check assumptions."
        color = "#ffc107"
    else:
        verdict = "🚨 HYPE ALERT — This exceeds physics-based projections."
        color = "#dc3545"
else:
    verdict = "📊 MODEL PREVIEW — No claim evaluated."
    color = "#007bff"

# Output boxes
st.markdown('<div class="box">', unsafe_allow_html=True)
st.markdown(f"**Chemistry Selected:** `{selected_chem}`")
st.markdown(f"**Projected Wh/kg (by {year}):** `{boosted:.1f}`")
st.markdown(f"**Mass per kWh:** `{kgpkwh:.2f} kg`")
st.markdown(f"**Scalability Assessment:** `{scalability}`")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="verdict-box" style="background-color:{color}; color:#fff;">{verdict}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("SP-VERT v1 by Science Police — Batteries over buzzwords.")
