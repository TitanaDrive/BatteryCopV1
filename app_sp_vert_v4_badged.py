
import streamlit as st
import json

st.set_page_config(page_title="SP-VERT v4", page_icon="⚡", layout="centered")
st.title("SP-VERT – Verified Battery Intelligence v4")
st.caption("Science Police certified: Truth over trend.")

# Load backend files
with open("SP_VERT_Benchmark_Backend.json", "r") as f:
    benchmarks = json.load(f)

with open("SP_VERT_Theoretical_Ranges.json", "r") as f:
    chem_ranges = json.load(f)

cell_benchmarks = benchmarks["cell_benchmarks_by_format"]
pack_benchmarks = benchmarks["pack_benchmarks_by_application"]

# Step 1: Chemistry
st.subheader("1. Choose Chemistry")
cathode = st.selectbox("Cathode", ["LFP", "NMC", "NCA", "LMFP", "NaFM", "NFPP", "Li–S", "Li–Air", "Na–Air"])
anode = st.selectbox("Anode", ["Graphite", "Si", "Hard Carbon", "Sn", "Li-metal", "Anode-Free"])

# Theoretical bounds (silent)
pair_key = f"{cathode}|{anode}"
theo_min, theo_max = chem_ranges.get(pair_key, (100, 600))

# Step 2: Theoretical Input (limited but no tooltip)
st.subheader("2. Input Theoretical Wh/kg")
theoretical = st.number_input("Max Theoretical Energy Density", min_value=theo_min, max_value=theo_max, value=theo_min)

# Step 3: Optional Lab Result
lab_density = st.number_input("Lab-Measured Energy Density (optional)", value=0.0)
lab_result = lab_density if lab_density > 0 else theoretical * 0.85

# Step 4: Engineered Cell Estimate
engineered = lab_result * 0.70

# Step 5: Format
st.subheader("3. Select Format")
format_selected = st.selectbox("Battery Format", list(cell_benchmarks.keys()))
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84
}
pack_result = engineered * format_eff[format_selected]

# Step 6: Application
st.subheader("4. Select Application")
application = st.selectbox("Application Target", list(pack_benchmarks.keys()))

# Compare with benchmark data
cell_threshold = cell_benchmarks.get(format_selected, 200)
pack_threshold = pack_benchmarks.get(application, 150)

# Badge logic
def badge(verdict):
    if verdict == "legend":
        return "🟩 **SP Badge: Science Legend** – Benchmark breaker!"
    elif verdict == "good":
        return "🟨 **SP Badge: Certified** – Within industry range"
    elif verdict == "weak":
        return "🟥 **SP Badge: Underperforming** – Needs revision"
    else:
        return "❓ **SP Badge: Unverified Combo** – Uncommon pairing"

cell_badge = "legend" if engineered > 1.05 * cell_threshold else "good" if engineered > 0.9 * cell_threshold else "weak"
pack_badge = "legend" if pack_result > 1.05 * pack_threshold else "good" if pack_result > 0.9 * pack_threshold else "weak"

# Final Display
st.subheader("5. Results Summary")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Theoretical:** {theoretical:.1f} Wh/kg")
st.markdown(f"- **Lab Result:** {lab_result:.1f} Wh/kg")
st.markdown(f"- **Engineered Cell:** {engineered:.1f} Wh/kg")
st.markdown(f"- **Pack Estimate ({format_selected}):** {pack_result:.1f} Wh/kg")
st.markdown(f"- **Application:** {application}")

# Verdicts
st.subheader("6. Verdicts & Badges")
st.markdown(f"- Cell Performance: {badge(cell_badge)}")
st.markdown(f"- Pack Performance: {badge(pack_badge)}")

st.caption("SP-VERT v4 – Powered by clean logic, real data, and certified science.")
