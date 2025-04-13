
import streamlit as st

st.set_page_config(page_title="Pack My Cell! – Advanced", page_icon="📦", layout="centered")
st.title("📦 Pack My Cell! – From Dream to Pack")
st.subheader("Track your battery's energy journey from theory to real-world pack")

# Step 1: Input theoretical energy density
theoretical = st.number_input("Theoretical max energy density (Wh/kg)", value=400)
lab_factor = 0.85
commercial_factor = 0.70

# Calculated stages
lab_density = theoretical * lab_factor
commercial_density = lab_density * commercial_factor

# Step 2: Select format
format_selected = st.selectbox("Select your pack format", ["Cylindrical", "Prismatic", "Pouch", "Blade"])
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84  # Based on Nature Comm. real data
}
pack_density = commercial_density * format_eff[format_selected]

# Show energy journey
st.markdown("### Energy Density Breakdown")
st.markdown(f"- **Theoretical Density:** {theoretical:.1f} Wh/kg")
st.markdown(f"- **Lab Achievable (×0.85):** {lab_density:.1f} Wh/kg")
st.markdown(f"- **Engineered Cell (×0.70):** {commercial_density:.1f} Wh/kg")
st.markdown(f"- **Pack Format Efficiency ({format_selected} ×{format_eff[format_selected]}):** {pack_density:.1f} Wh/kg")

# SP Verdict
if pack_density >= 180:
    st.success("✅ Excellent! Your chemistry scales beautifully.")
elif 120 <= pack_density < 180:
    st.warning("⚠️ Decent. Could be tighter in real-world packaging.")
else:
    st.error("🚨 Weak pack performance. Is your design viable at scale?")

# References
st.markdown("---")
st.markdown("#### References")
st.markdown("- Nature Communications 2024: Verified Blade battery CTP pack = 135 Wh/kg from 160 Wh/kg cell (84%)")
st.markdown("- Industry norms: Cylindrical ~60%, Pouch ~80%, Prismatic ~75%")

st.caption("Pack My Cell! by Science Police – Because energy doesn't stop at the cell.")
