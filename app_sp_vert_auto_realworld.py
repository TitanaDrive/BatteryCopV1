
import streamlit as st
import json

st.set_page_config(page_title="SP-VERT Auto Edition", page_icon="🚗", layout="centered")
st.title("SP-VERT – Auto Edition")
st.caption("Science Police Certified | Auto Benchmark Enforcement Active")

# Load cell-level thresholds (hidden logic)
with open("SP_VERT_Benchmark_Backend.json", "r") as f:
    benchmarks = json.load(f)
with open("SP_VERT_Theoretical_Ranges.json", "r") as f:
    chem_ranges = json.load(f)

cell_benchmarks = benchmarks["cell_benchmarks_by_format"]

# Real-world EV pack references per format
format_refs = {
    "Cylindrical": 167,
    "Prismatic": 148,
    "Pouch": 156,
    "Blade": 151
}

# Step 1: Auto-grade chemistry
st.subheader("1. Choose Auto-Grade Chemistry")
auto_chemistries = [
    ("LFP", "Graphite"),
    ("NMC", "Graphite"),
    ("NMC", "Si"),
    ("NCA", "Graphite"),
    ("LMFP", "Graphite"),
    ("LMFP", "Si")
]
chem_option = st.selectbox("Cathode | Anode", [f"{c}|{a}" for c, a in auto_chemistries])
cathode, anode = chem_option.split("|")
pair_key = f"{cathode}|{anode}"
theo_min, theo_max = chem_ranges.get(pair_key, (100, 600))

# Step 2: User input
st.subheader("2. Input Lab Energy Data")
theoretical = st.number_input("Theoretical Energy Density (Wh/kg)", value=theo_min, min_value=theo_min, max_value=theo_max)
lab_density = st.number_input("Lab-Measured Energy Density (optional)", value=0.0)
lab_result = lab_density if lab_density > 0 else theoretical * 0.85
engineered = lab_result * 0.70

# Step 3: Format
st.subheader("3. Select Format")
format_selected = st.selectbox("Battery Format", list(format_refs.keys()))
real_pack_reference = format_refs.get(format_selected, 150)

# SP badge logic
def badge(value, benchmark):
    if value > 1.05 * benchmark:
        return "🟩 **SP Badge: Road Legend** – You outperform Tesla."
    elif value >= 0.9 * benchmark:
        return "🟨 **SP Badge: Road Certified** – On par with industry"
    else:
        return "🟥 **SP Badge: Underperforming** – Below EV-grade"

# Output
st.subheader("4. Results & Verdicts")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Theoretical:** {theoretical:.1f} Wh/kg")
st.markdown(f"- **Lab Result:** {lab_result:.1f} Wh/kg")
st.markdown(f"- **Engineered Cell:** {engineered:.1f} Wh/kg")
st.markdown(f"- **Estimated Pack Gravimetric (format-based):** {engineered:.1f} Wh/kg")

st.subheader("5. SP Verdict")
st.markdown(badge(engineered, real_pack_reference))

# Signature
st.markdown("---")
st.markdown("**Verified by: Science Police – Tesla, Ivana**  \
*“If it packs nonsense, we pack it up.”*")
st.caption("SP-VERT Auto Edition – Format-aware, benchmark-enforced, hype-proof.")
