
import streamlit as st

st.set_page_config(page_title="SP-VERT Unified", page_icon="🔍", layout="centered")
st.title("SP-VERT – Unified Battery Verificator")
st.caption("Step-by-step validation: From chemistry to commercial reality")

# Step 1: Chemistry
st.markdown("### 1. Choose Chemistry")
cathode = st.selectbox("Cathode Material", ["LFP", "NMC", "NCA", "LMFP", "NaFM", "NFPP", "Li–S", "Li–Air", "Na–Air"])
anode = st.selectbox("Anode Material", ["Graphite", "Si", "Hard Carbon", "Sn", "Li-metal", "Anode-Free"])

# Step 2: Theoretical Capacity
st.markdown("### 2. Input Theoretical Energy Density")
theoretical = st.number_input("Theoretical Wh/kg", value=400)

# Step 3: Lab Measured
lab_density = st.number_input("Lab-measured Energy Density (optional)", value=0.0)
lab_result = lab_density if lab_density > 0 else theoretical * 0.85

# Step 4: Engineered Cell Estimate
engineered = lab_result * 0.70

# Step 5: Format
st.markdown("### 3. Select Format")
format_selected = st.selectbox("Battery Format", ["Cylindrical", "Prismatic", "Pouch", "Blade"])
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84
}
pack_result = engineered * format_eff[format_selected]

# Step 6: Application
st.markdown("### 4. Select Application")
application = st.selectbox("Target Application", ["EV", "ESS", "Drone", "Power Tool", "Aerospace"])

# Step 7: Compare with Market
st.markdown("### 5. Pack Benchmark Comparison")
benchmarks = {
    "Tesla Model 3 (21700)": 167,
    "BYD Blade (LFP)": 151,
    "Hyundai Ioniq 5 (Pouch)": 156,
    "BMW i4 (Prismatic)": 148,
    "CATL Qilin (NMC)": 205
}
for model, value in benchmarks.items():
    st.markdown(f"- **{model}:** {value} Wh/kg")

# Results
st.markdown("### Final Output")
st.markdown(f"- **Chemistry:** {cathode} | {anode}")
st.markdown(f"- **Theoretical Wh/kg:** {theoretical}")
st.markdown(f"- **Lab Result:** {lab_result:.1f}")
st.markdown(f"- **Cell (engineered):** {engineered:.1f}")
st.markdown(f"- **Pack ({format_selected}):** {pack_result:.1f}")
st.markdown(f"- **Application:** {application}")

# Verdict
if pack_result >= 180:
    st.success("✅ High-performing pack! Ready to challenge the market.")
elif 120 <= pack_result < 180:
    st.warning("⚠️ Acceptable, but room for design or format improvement.")
else:
    st.error("🚨 Below-market pack performance. Needs revision.")

st.caption("SP-VERT by Science Police – Truth. Verified.")
