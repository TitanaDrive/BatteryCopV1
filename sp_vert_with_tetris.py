
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="SP-VERT – Unified Battery Verificator", page_icon="🔬", layout="wide")
st.title("SP-VERT – Unified Battery Verificator")
st.caption("From chemistry to credibility – now with Battery Tetris visual validation")

# Step 1: Chemistry Input
st.sidebar.header("Step 1: Chemistry Selection")
cathode = st.sidebar.selectbox("Cathode", ["LFP", "NMC", "LMFP", "LCO", "NCA"])
anode = st.sidebar.selectbox("Anode", ["Graphite", "Silicon", "LTO", "Li-metal"])

# Step 2: TRL and Capacity Input
st.sidebar.header("Step 2: Technology Readiness Level (TRL)")
trl = st.sidebar.selectbox("TRL", ["Theoretical", "Lab", "Commercial"])

st.sidebar.header("Step 3: Energy Density Input")
theoretical_ed = st.sidebar.number_input("Theoretical Energy Density (Wh/kg)", min_value=50.0, max_value=500.0, value=250.0)
measured_ed = st.sidebar.number_input("Measured (Lab/Real) Energy Density (Wh/kg)", min_value=0.0, max_value=500.0, value=0.0)

# Step 4: Format Selection
st.sidebar.header("Step 4: Cell Format")
format_selected = st.sidebar.selectbox("Format", ["Blade", "Prismatic", "Pouch", "2170", "4680"])

# Step 5: Application
application = st.sidebar.selectbox("Step 5: Application", ["Automotive", "ESS", "Other"])

# Logic Check (Silent backend capacity validation – not shown to user)
valid_combinations = {
    ("LFP", "Graphite"): (100, 180),
    ("NMC", "Graphite"): (150, 250),
    ("NMC", "Silicon"): (200, 300),
    ("LFP", "LTO"): (60, 120),
    ("NCA", "Graphite"): (180, 270),
}

if (cathode, anode) in valid_combinations:
    min_ed, max_ed = valid_combinations[(cathode, anode)]
    if theoretical_ed > max_ed:
        st.error("Theoretical energy density exceeds realistic maximum for this chemistry combo.")
    elif theoretical_ed < min_ed:
        st.warning("Theoretical energy density is below known benchmark values.")

# Results Summary
st.markdown(f"### Summary")
st.markdown(f"- **Cathode:** {cathode}")
st.markdown(f"- **Anode:** {anode}")
st.markdown(f"- **TRL:** {trl}")
st.markdown(f"- **Theoretical ED:** {theoretical_ed} Wh/kg")
st.markdown(f"- **Measured ED:** {measured_ed if measured_ed > 0 else 'N/A'}")
st.markdown(f"- **Format:** {format_selected}")
st.markdown(f"- **Application:** {application}")

# Battery Tetris Visualizer
st.markdown("## Battery Tetris – Visual Format Packing")
st.caption("See how your chosen format packs inside a standard automotive module")

# Set default module size for auto
module_w, module_h = 10, 6

# Cell dimensions (normalized)
cell_shapes = {
    "Blade": {"w": 2.5, "h": 0.5, "color": "#D3E4CD"},
    "Prismatic": {"w": 2.2, "h": 1.2, "color": "#FFC898"},
    "Pouch": {"w": 2.0, "h": 0.8, "color": "#AEDFF7"},
    "2170": {"w": 1.0, "h": 1.0, "color": "#F6C6EA"},
    "4680": {"w": 2.0, "h": 2.0, "color": "#C8A2C8"},
}

# Draw Tetris-style layout
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, module_w)
ax.set_ylim(0, module_h)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Packing Simulation", fontsize=14, weight='bold')

ax.add_patch(patches.Rectangle((0, 0), module_w, module_h, edgecolor='black', facecolor='#F5F5F5', linewidth=2))

cw, ch = cell_shapes[format_selected]["w"], cell_shapes[format_selected]["h"]
col = cell_shapes[format_selected]["color"]
count = 0
y = 0
while y + ch <= module_h:
    x = 0
    while x + cw <= module_w:
        ax.add_patch(patches.FancyBboxPatch((x, y), cw, ch, boxstyle="round,pad=0.02",
                                            facecolor=col, edgecolor='black', linewidth=1.2))
        count += 1
        x += cw
    y += ch

ax.text(module_w - 0.2, module_h - 0.2, "SP", fontsize=16, color='darkred', weight='bold', ha='right', va='top')

# Efficiency calc
box_area = module_w * module_h
cell_area = cw * ch
filled_area = count * cell_area
efficiency = (filled_area / box_area) * 100

st.pyplot(fig)
st.markdown(f"### Packing Efficiency: **{efficiency:.1f}%** with {count} cells")
st.caption("Science Police – Packing the truth.")
