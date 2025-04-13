
import streamlit as st

st.set_page_config(page_title="SP-VERT – Scalability Mode", page_icon="🔋", layout="centered")

st.title("SP-VERT – Battery Scalability Checker")
st.caption("Cathode–Anode Combo Evaluator v1.1 (Safe version)")

# Chemistry database
chemistry_data = {"LFP | Graphite": {"Wh/kg": 150, "kg/kWh": 6.5, "scalability": "Scalable \u2013 Abundant Fe, P, moderate Li"}, "NMC | Graphite": {"Wh/kg": 220, "kg/kWh": 4.5, "scalability": "Aggressive \u2013 Ni, Co constraints"}, "NCA | Si-anode": {"Wh/kg": 250, "kg/kWh": 4.0, "scalability": "Aggressive \u2013 Ni/Si tradeoffs"}, "LMFP | Si-anode": {"Wh/kg": 230, "kg/kWh": 4.8, "scalability": "Scalable \u2013 No Co/Ni, abundant elements"}, "NaFM | HC": {"Wh/kg": 134, "kg/kWh": 7.5, "scalability": "Scalable \u2013 No critical metals"}, "NaNM | HC": {"Wh/kg": 134, "kg/kWh": 7.5, "scalability": "Scalable \u2013 Abundant Mn/Fe"}, "NaFM | Sn": {"Wh/kg": 185, "kg/kWh": 5.4, "scalability": "Limited \u2013 Tin bottleneck"}, "NFPP | HC": {"Wh/kg": 111, "kg/kWh": 9.0, "scalability": "Scalable \u2013 Earth-abundant"}, "NaNM | Anode-Free": {"Wh/kg": 207, "kg/kWh": 4.8, "scalability": "Emerging \u2013 Efficiency + scaling challenges"}, "NaSICON | HC": {"Wh/kg": 150, "kg/kWh": 6.0, "scalability": "Aggressive \u2013 Vanadium limited"}, "Li\u2013S": {"Wh/kg": 350, "kg/kWh": 3.3, "scalability": "Scalable \u2013 Sulfur abundant, tech challenges remain"}, "Li\u2013Air": {"Wh/kg": 3500, "kg/kWh": 0.3, "scalability": "Hype \u2013 Not commercially viable yet"}, "Na\u2013Air": {"Wh/kg": 1200, "kg/kWh": 0.8, "scalability": "Hype \u2013 Early-stage concept"}}

# Inputs
selected_chem = st.selectbox("Choose chemistry pair", list(chemistry_data.keys()))
roadmap_year = st.slider("Roadmap year", 2024, 2040, 2025)
claim = st.number_input("Claimed energy (Wh/kg)", value=0)

# Extract baseline and compute
base = chemistry_data[selected_chem]
boosted = base["Wh/kg"] + (roadmap_year - 2025) * 2
claimed = claim if claim > 0 else boosted
kgpkwh = base["kg/kWh"]
scalability = base["scalability"]

# Verdict engine
if claim > 0:
    if claim <= boosted * 1.1:
        verdict = "REALISTIC"
        color = "#28a745"
    elif claim <= boosted * 1.3:
        verdict = "AGGRESSIVE"
        color = "#ffc107"
    else:
        verdict = "HYPE"
        color = "#dc3545"
else:
    verdict = "MODEL PREVIEW"
    color = "#007bff"

# Output layout
st.markdown("### Evaluation Result")
st.markdown(f"**Projected energy (Wh/kg):** {boosted:.1f}")
st.markdown(f"**Material demand per 1 kWh:** {kgpkwh:.2f} kg")
st.markdown("**Scalability tag:** " + scalability)

st.markdown(f'<div style="background-color:{color};padding:12px;border-radius:10px;color:#fff;text-align:center;font-size:20px;">{verdict}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("SP-VERT by Science Police – Version 1.1 – All rights reserved.")
