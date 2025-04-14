
import streamlit as st
import json

st.set_page_config(page_title="SP-VERT Auto Edition", page_icon="🚗", layout="centered")
st.title("SP-VERT – Auto Edition")
st.caption("Certified for road-readiness by Science Police | Tesla, Ivana")

# Load benchmark data
with open("SP_VERT_Benchmark_Backend.json", "r") as f:
    benchmarks = json.load(f)

cell_benchmarks = benchmarks["cell_benchmarks_by_format"]
pack_benchmarks = benchmarks["pack_benchmarks_by_application"]

# Automotive presets
auto_chemistries = [
    ("LFP", "Graphite"),
    ("NMC", "Graphite"),
    ("NMC", "Si"),
    ("NCA", "Graphite"),
    ("LMFP", "Graphite"),
    ("LMFP", "Si")
]

# Step 1: Select automotive chemistry
st.subheader("1. Choose Your Auto-Grade Chemistry")
chem_option = st.selectbox("Cathode | Anode Pair", [f"{c}|{a}" for c, a in auto_chemistries])
cathode, anode = chem_option.split("|")

# Step 2: Enter lab result (or auto-calculate)
st.subheader("2. Input Lab-Measured Cell Energy Density")
lab_density = st.number_input("Lab Energy Density (Wh/kg)", value=200.0, min_value=100.0, max_value=400.0)

# Step 3: Cell format (auto-relevant only)
st.subheader("3. Select Format Used in EV Packs")
format_selected = st.selectbox("Format", ["Cylindrical", "Prismatic", "Pouch", "Blade"])
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84
}

# Estimate pack-level performance
engineered = lab_density * 0.70
pack_result = engineered * format_eff[format_selected]

# Step 4: Compare with real EV pack benchmarks
st.subheader("4. Application Benchmark: EV Pack Comparison")
ev_pack_threshold = pack_benchmarks.get("EV", 150)

# Results
st.markdown("### Final Report")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Lab Result:** {lab_density:.1f} Wh/kg")
st.markdown(f"- **Engineered Cell:** {engineered:.1f} Wh/kg")
st.markdown(f"- **Pack Estimate ({format_selected}):** {pack_result:.1f} Wh/kg")

# Verdict
if pack_result > 1.1 * ev_pack_threshold:
    st.success("🟩 SP Verdict: Road-Dominant! Benchmark surpassed.")
elif pack_result >= 0.9 * ev_pack_threshold:
    st.warning("🟨 SP Verdict: Road-Ready. Meets market standards.")
else:
    st.error("🟥 SP Verdict: Needs Retuning. Pack underperforms for EV use.")

# Signature
st.markdown("---")
st.markdown("**Verified by: Science Police**  
*Tesla, Ivana*  
'If it packs nonsense, we pack it up.'")

st.caption("SP-VERT Auto Edition – Designed for real engineers building real vehicles.")
