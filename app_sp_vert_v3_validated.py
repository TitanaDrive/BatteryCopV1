
import streamlit as st
import json

st.set_page_config(page_title="SP-VERT v3 – Chemistry Validated", page_icon="🧪", layout="centered")
st.title("SP-VERT – Unified Battery Verificator v3")
st.caption("Science Police: Chemistry-aware validation active")

# Load backend files
with open("SP_VERT_Benchmark_Backend.json", "r") as f:
    benchmarks = json.load(f)

with open("SP_VERT_Theoretical_Ranges.json", "r") as f:
    chem_ranges = json.load(f)

cell_benchmarks = benchmarks["cell_benchmarks_by_format"]
pack_benchmarks = benchmarks["pack_benchmarks_by_application"]

# Step 1: Chemistry
st.markdown("### 1. Choose Chemistry")
cathode = st.selectbox("Cathode Material", ["LFP", "NMC", "NCA", "LMFP", "NaFM", "NFPP", "Li–S", "Li–Air", "Na–Air"])
anode = st.selectbox("Anode Material", ["Graphite", "Si", "Hard Carbon", "Sn", "Li-metal", "Anode-Free"])

pair_key = f"{cathode}|{anode}"
theo_min, theo_max = chem_ranges.get(pair_key, (100, 500))

# Step 2: Theoretical Capacity
st.markdown(f"### 2. Input Theoretical Energy Density ({theo_min}-{theo_max} Wh/kg expected)")
theoretical = st.number_input("Your theoretical Wh/kg", value=theo_min, min_value=theo_min, max_value=theo_max)

# Step 3: Lab Result (optional)
lab_density = st.number_input("Lab-measured Energy Density (optional)", value=0.0)
lab_result = lab_density if lab_density > 0 else theoretical * 0.85

# Step 4: Engineered Cell Estimate
engineered = lab_result * 0.70

# Step 5: Format
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

# Step 7: Output & silent validation
cell_threshold = cell_benchmarks.get(format_selected, 200)
pack_threshold = pack_benchmarks.get(application, 150)

# Results
st.markdown("### Final Output")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Theoretical Energy:** {theoretical:.1f} Wh/kg")
st.markdown(f"- **Lab Result:** {lab_result:.1f} Wh/kg")
st.markdown(f"- **Cell (engineered):** {engineered:.1f} Wh/kg")
st.markdown(f"- **Estimated Pack ({format_selected}):** {pack_result:.1f} Wh/kg")
st.markdown(f"- **Application:** {application}")

# Verdict Logic
if engineered < 0.9 * cell_threshold:
    st.error("🚨 Cell-level performance below benchmark.")
elif engineered < 1.05 * cell_threshold:
    st.warning("⚠️ Cell performance in expected range.")
else:
    st.success("✅ Strong cell vs. market average.")

if pack_result < 0.9 * pack_threshold:
    st.error("🚨 Pack result too low for application.")
elif pack_result < 1.05 * pack_threshold:
    st.warning("⚠️ Acceptable pack performance.")
else:
    st.success("✅ Competitive pack performance!")

st.caption("SP-VERT v3 – No nonsense. Chemistry verified.")
