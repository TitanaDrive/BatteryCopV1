
import streamlit as st
import json

st.set_page_config(page_title="SP-VERT Auto Edition", page_icon="🚗", layout="centered")
st.title("SP-VERT – Auto Edition")
st.caption("Science Police Certified | Automotive Battery Verification Tool")

# Load backend benchmark data
with open("SP_VERT_Benchmark_Backend.json", "r") as f:
    benchmarks = json.load(f)
with open("SP_VERT_Theoretical_Ranges.json", "r") as f:
    chem_ranges = json.load(f)

cell_benchmarks = benchmarks["cell_benchmarks_by_format"]
pack_benchmarks = benchmarks["pack_benchmarks_by_application"]

# Step 1: Auto-Grade Chemistry
st.subheader("1. Choose Automotive Chemistry")
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

# Silent theoretical validation
pair_key = f"{cathode}|{anode}"
theo_min, theo_max = chem_ranges.get(pair_key, (100, 600))

# Step 2: Input (restricted but not visible to user)
st.subheader("2. Enter Lab-Verified Cell Energy Density")
theoretical = st.number_input("Theoretical Energy Density (Wh/kg)", value=theo_min, min_value=theo_min, max_value=theo_max)
lab_density = st.number_input("Lab-Measured Energy Density (optional)", value=0.0)
lab_result = lab_density if lab_density > 0 else theoretical * 0.85
engineered = lab_result * 0.70

# Step 3: Format (only auto-valid)
st.subheader("3. Choose Cell Format for EV Pack")
format_selected = st.selectbox("Format", ["Cylindrical", "Prismatic", "Pouch", "Blade"])
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84
}
pack_result = engineered * format_eff[format_selected]

# Step 4: Application fixed to EV
application = "EV"
cell_threshold = cell_benchmarks.get(format_selected, 200)
pack_threshold = pack_benchmarks.get(application, 150)

# SP Badge Logic
def badge(verdict):
    if verdict == "legend":
        return "🟩 **SP Badge: Road Legend** – Benchmark breaker!"
    elif verdict == "good":
        return "🟨 **SP Badge: Road Ready** – On par with current market"
    elif verdict == "weak":
        return "🟥 **SP Badge: Needs Retuning** – Rework required"
    else:
        return "❓ **SP Badge: Undocumented Combo**"

cell_badge = "legend" if engineered > 1.05 * cell_threshold else "good" if engineered > 0.9 * cell_threshold else "weak"
pack_badge = "legend" if pack_result > 1.05 * pack_threshold else "good" if pack_result > 0.9 * pack_threshold else "weak"

# Results Summary
st.subheader("4. Final Evaluation")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Theoretical Energy:** {theoretical:.1f} Wh/kg")
st.markdown(f"- **Lab Result:** {lab_result:.1f} Wh/kg")
st.markdown(f"- **Engineered Cell:** {engineered:.1f} Wh/kg")
st.markdown(f"- **Pack Estimate ({format_selected}):** {pack_result:.1f} Wh/kg")

# Verdicts
st.subheader("5. SP Verdicts")
st.markdown(f"- Cell Performance: {badge(cell_badge)}")
st.markdown(f"- Pack Performance: {badge(pack_badge)}")

# Signature
st.markdown("---")
st.markdown("**Verified by: Science Police – Tesla, Ivana**  \
*“If it packs nonsense, we pack it up.”*")
st.caption("SP-VERT Auto Edition – Full logic, road focused.")

