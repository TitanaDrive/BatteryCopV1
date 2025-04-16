
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Battery Tetris – SP Edition", page_icon="🔋", layout="wide")
st.title("Battery Tetris – Science Police Edition")
st.caption("Pack like a pro. Compare formats. Enforce reality.")

# Sidebar inputs
st.sidebar.header("1. Select Module Size")
preset = st.sidebar.radio("Preset Module Type", ["Mini EV", "Sedan", "SUV", "Custom"])

if preset == "Mini EV":
    module_w, module_h = 6, 4
elif preset == "Sedan":
    module_w, module_h = 10, 6
elif preset == "SUV":
    module_w, module_h = 12, 8
else:
    module_w = st.sidebar.slider("Custom Width (cells)", 4, 20, 10)
    module_h = st.sidebar.slider("Custom Height (cells)", 3, 12, 6)

st.sidebar.markdown("---")
format_selected = st.sidebar.selectbox("2. Select Cell Format", ["Blade", "Prismatic", "Pouch", "2170", "4680"])

st.sidebar.markdown("**SP Branding Active**")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Battery_icon.svg/1024px-Battery_icon.svg.png", width=60)

# Cell dimensions (normalized for visualization)
cell_shapes = {
    "Blade": {"w": 2.5, "h": 0.5, "color": "#D3E4CD"},
    "Prismatic": {"w": 2.2, "h": 1.2, "color": "#FFC898"},
    "Pouch": {"w": 2.0, "h": 0.8, "color": "#AEDFF7"},
    "2170": {"w": 1.0, "h": 1.0, "color": "#F6C6EA"},
    "4680": {"w": 2.0, "h": 2.0, "color": "#C8A2C8"},
}

# Draw simulation
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, module_w)
ax.set_ylim(0, module_h)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Packing Simulation", fontsize=14, weight='bold')

# Module outline
ax.add_patch(patches.Rectangle((0, 0), module_w, module_h, edgecolor='black', facecolor='#F5F5F5', linewidth=2))

# Cell placement (Auto pack from bottom-left to top-right)
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

# SP branding
ax.text(module_w - 0.2, module_h - 0.2, "SP", fontsize=16, color='darkred', weight='bold', ha='right', va='top')

# Efficiency Calculation
box_area = module_w * module_h
cell_area = cw * ch
filled_area = count * cell_area
efficiency = (filled_area / box_area) * 100

st.pyplot(fig)
st.markdown(f"### Packing Efficiency: **{efficiency:.1f}%** with {count} cells")
st.caption("Battery Tetris – The truth is in the shape.")
