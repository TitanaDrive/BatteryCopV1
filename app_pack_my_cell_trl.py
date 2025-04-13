
import streamlit as st

st.set_page_config(page_title="Pack My Cell! – TRL Edition", page_icon="⚙️", layout="centered")
st.title("⚙️ Pack My Cell!")
st.subheader("From theory to pack – track your cell’s potential")

st.markdown("### Step 1: Enter what you know")

# Input theoretical value (always required)
theoretical = st.number_input("Max theoretical energy density (Wh/kg)", value=400)

# Optional inputs based on TRL
lab_density = st.number_input("Measured lab energy density (optional)", value=0.0)
cell_density = st.number_input("Commercial-level cell energy density (optional)", value=0.0)

# Format choice
format_selected = st.selectbox("Select pack format", ["Cylindrical", "Prismatic", "Pouch", "Blade"])
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.84  # from Nature Comm
}

# Auto progress based on inputs
used_lab = lab_density if lab_density > 0 else theoretical * 0.85
used_cell = cell_density if cell_density > 0 else used_lab * 0.70
pack_density = used_cell * format_eff[format_selected]

# Display outputs
st.markdown("### Energy Journey")
st.markdown(f"- **Theoretical Max:** {theoretical:.1f} Wh/kg")
if lab_density > 0:
    st.markdown(f"- **Your Lab Result:** {lab_density:.1f} Wh/kg")
else:
    st.markdown(f"- *Estimated Lab Result (~85%):* {used_lab:.1f} Wh/kg")
if cell_density > 0:
    st.markdown(f"- **Your Engineered Cell:** {cell_density:.1f} Wh/kg")
else:
    st.markdown(f"- *Estimated Commercial Cell (~70%):* {used_cell:.1f} Wh/kg")
st.markdown(f"- **Final Pack Estimate ({format_selected}):** {pack_density:.1f} Wh/kg")

# SP-style feedback
if pack_density >= 180:
    st.success("✅ Scalable potential! Keep pushing.")
elif pack_density >= 120:
    st.warning("⚠️ Moderate. Might struggle in real-world packaging.")
else:
    st.error("🚨 Low pack-level energy. Time to rethink or optimize.")

# Reference examples
st.markdown("---")
st.markdown("### Real-World References")
st.markdown("- **Blade (LFP):** 160 → 135 Wh/kg")
st.markdown("- **21700 (NMC):** 250 → 150 Wh/kg")
st.markdown("- **CATL Qilin (NMC):** 255 → 205 Wh/kg")

st.caption("Built by Science Police – Reality, not fantasy.")
