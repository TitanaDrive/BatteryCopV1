
import streamlit as st
import json

st.set_page_config(page_title="SP-VERT Unified v2", page_icon="🔍", layout="centered")
st.title("SP-VERT – Unified Battery Verificator v2")
st.caption("From chemistry to credibility – Science Police certified")

# Load backend benchmark data
with open("SP_VERT_Benchmark_Backend.json", "r") as f:
    benchmarks = json.load(f)

cell_benchmarks = benchmarks["cell_benchmarks_by_format"]
pack_benchmarks = benchmarks["pack_benchmarks_by_application"]

# Step 1: Chemistry
st.markdown("### 1. Choose Chemistry")
cathode = st.selectbox("Cathode Material", ["LFP", "NMC", "NCA", "LMFP", "NaFM", "NFPP", "Li–S", "Li–Air", "Na–Air"])
anode = st.selectbox("Anode Material", ["Graphite", "Si", "Hard Carbon", "Sn", "Li-metal", "Anode-Free"])

# Step 2: Theoretical Capacity
st.markdown("### 2. Input Theoretical Energy Density")
theoretical = st.number_input("Theoretical Wh/kg", value=400)

# Step 3: Lab Measured (optional)
lab_density = st.number_input("Lab-measured Energy Density", value=0.0)
lab_result = lab_density if lab_density > 0 else theoretical * 0.85

# Step 4: Estimate engineered cell performance
engineered = lab_result * 0.70

# Step 5: Cell format
st.markdown("### 3. Select Format")
format_selected = st.selectbox("Battery Format", list(cell_benchmarks.keys()))
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84
}
pack_result = engineered * format_eff[format_selected]

# Step 6: Application
st.markdown("### 4. Select Application")
application = st.selectbox("Target Application", list(pack_benchmarks.keys()))

# Step 7: Silent backend validation
cell_threshold = cell_benchmarks.get(format_selected, 200)
pack_threshold = pack_benchmarks.get(application, 150)

# Step 8: Feedback logic
st.markdown("### Final Results")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Theoretical Energy:** {theoretical:.1f} Wh/kg")
st.markdown(f"- **Lab Result:** {lab_result:.1f} Wh/kg")
st.markdown(f"- **Engineered Cell:** {engineered:.1f} Wh/kg")
st.markdown(f"- **Estimated Pack ({format_selected}):** {pack_result:.1f} Wh/kg")
st.markdown(f"- **Application:** {application}")

# Verdict logic (cell first, then pack)
if engineered < 0.9 * cell_threshold:
    st.error("🚨 Cell-level performance below industry benchmark.")
elif engineered < 1.05 * cell_threshold:
    st.warning("⚠️ Cell performance in range, but not best-in-class.")
else:
    st.success("✅ Strong cell performance vs market.")

if pack_result < 0.9 * pack_threshold:
    st.error("🚨 Pack performance below market average.")
elif pack_result < 1.05 * pack_threshold:
    st.warning("⚠️ Pack performance acceptable, but improvable.")
else:
    st.success("✅ Your pack can compete in today’s market.")

st.caption("Powered by Science Police – v2 backend with live benchmarks.")
