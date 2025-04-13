
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Battery Tetris – SP Edition", page_icon="🧩", layout="centered")
st.title("🔋 Battery Tetris – Module Packing Visualizer")
st.caption("See how different cell formats pack inside a module")

# Module box size
module_width = 10
module_height = 6

# Cell geometries (in grid units)
cell_shapes = {
    "Cylindrical": (1, 2),
    "Prismatic": (2, 2),
    "Pouch": (2, 3),
    "Blade": (1, 6)
}

selected_format = st.selectbox("Select cell format to simulate", list(cell_shapes.keys()))
cell_w, cell_h = cell_shapes[selected_format]

# Calculate fit into box
fit_cols = module_width // cell_w
fit_rows = module_height // cell_h
cell_count = fit_cols * fit_rows
used_area = cell_count * (cell_w * cell_h)
total_area = module_width * module_height
efficiency = used_area / total_area

# Draw visual
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_xlim(0, module_width)
ax.set_ylim(0, module_height)
ax.set_aspect('equal')
ax.axis('off')

# Fill module with cells
for row in range(fit_rows):
    for col in range(fit_cols):
        x = col * cell_w
        y = row * cell_h
        rect = plt.Rectangle((x, y), cell_w, cell_h, edgecolor='black', facecolor='skyblue')
        ax.add_patch(rect)

# Outline the module box
ax.add_patch(plt.Rectangle((0, 0), module_width, module_height, edgecolor='black', fill=False, linewidth=2))

st.pyplot(fig)

# Efficiency readout
st.markdown(f"**Cells packed:** {cell_count}")
st.markdown(f"**Packing efficiency:** {efficiency*100:.1f}% of module area")
st.caption("Visualized in 2D grid units. Full 3D coming soon!")
