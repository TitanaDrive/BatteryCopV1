
import streamlit as st
import pandas as pd

# Title
st.title("SP-VERT: Battery Scalability Checker")
st.subheader("Science Police Verdict Engine v1")

# Chemistry database with placeholder values (to be replaced by real mass balance and resource data)
chemistry_data = {
    "NaFM | HC": {"Wh/kg": 134, "kg/kWh": 7.46, "resource_flag": "SCALABLE"},
    "NaNM | HC": {"Wh/kg": 134, "kg/kWh": 7.46, "resource_flag": "SCALABLE"},
    "NaFM | Sn": {"Wh/kg": 185, "kg/kWh": 5.4, "resource_flag": "LIMITED - Tin"},
    "NFPP | HC": {"Wh/kg": 111, "kg/kWh": 9.01, "resource_flag": "SCALABLE"},
    "LFP | Graphite": {"Wh/kg": 160, "kg/kWh": 6.25, "resource_flag": "SCALABLE"},
    "NMC | Graphite": {"Wh/kg": 250, "kg/kWh": 4.0, "resource_flag": "CONSTRAINED - Ni, Co"},
    "NMC | Si": {"Wh/kg": 300, "kg/kWh": 3.33, "resource_flag": "AGGRESSIVE - Ni, Si"},
    "NaNM | Anode-Free": {"Wh/kg": 207, "kg/kWh": 4.8, "resource_flag": "LIMITED - Anode challenges"},
}

# Inputs
selected_chem = st.selectbox("Choose chemistry pair", list(chemistry_data.keys()))
roadmap_year = st.slider("Select roadmap year", 2024, 2040, 2025)
claim = st.number_input("Enter claimed Wh/kg (optional)", value=0)

# Logic for adjusting performance
base = chemistry_data[selected_chem]
improved_whkg = base["Wh/kg"] + (roadmap_year - 2025) * 2
claimed = claim if claim > 0 else improved_whkg
kg_kwh = base["kg/kWh"]
scalability = base["resource_flag"]

# Verdict logic
if claim > 0:
    if claim <= improved_whkg * 1.1:
        verdict = "✅ Realistic"
    elif claim <= improved_whkg * 1.3:
        verdict = "⚠️ Aggressive"
    else:
        verdict = "🚨 Hype"
else:
    verdict = "Model Preview"

# Display
st.markdown(f"### Selected Chemistry: `{selected_chem}`")
st.markdown(f"- **Projected Wh/kg**: {improved_whkg:.1f}")
st.markdown(f"- **Mass per kWh (kg)**: {kg_kwh:.2f}")
st.markdown(f"- **Scalability Tag**: {scalability}")
st.markdown(f"## Verdict: {verdict}")
