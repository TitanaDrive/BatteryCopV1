
import streamlit as st

st.set_page_config(page_title="Pack My Cell!", page_icon="📦", layout="centered")
st.title("📦 Pack My Cell!")
st.subheader("How will YOUR cell perform at pack level?")

# Input from user
cell_whkg = st.number_input("Enter your cell's energy density (Wh/kg)", value=150)
format_selected = st.selectbox("Select your battery format", ["Cylindrical", "Prismatic", "Pouch", "Blade"])

# Format efficiencies
format_eff = {
    "Cylindrical": 0.60,
    "Prismatic": 0.75,
    "Pouch": 0.80,
    "Blade": 0.88
}

# Calculation
efficiency = format_eff[format_selected]
pack_whkg = cell_whkg * efficiency

# Display results
st.markdown("### Results")
st.markdown(f"**Cell-level energy density:** {cell_whkg:.1f} Wh/kg")
st.markdown(f"**Format efficiency:** {efficiency*100:.0f}%")
st.markdown(f"**Estimated pack-level energy density:** **{pack_whkg:.1f} Wh/kg**")

# Verdict tone
if pack_whkg >= 180:
    st.success("✅ Strong performance! Your pack is lean and mean.")
elif 120 <= pack_whkg < 180:
    st.warning("⚠️ Moderate efficiency. Room for improvement.")
else:
    st.error("🚨 Low pack performance! Might be time to rethink your format or chemistry.")

st.markdown("---")
st.caption("Built by Science Police — Making battery specs make sense.")
