
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Battery Tetris – Plotly Edition", page_icon="🧩", layout="centered")
st.title("🔋 Battery Tetris – Pack Layout Visualizer")
st.caption("Visualize 2D packing of battery formats inside a module")

# Module box dimensions (grid units)
module_width = 10
module_height = 6

# Cell format sizes
cell_shapes = {
    "Cylindrical": (1, 2),
    "Prismatic": (2, 2),
    "Pouch": (2, 3),
    "Blade": (1, 6)
}

# Select format
selected_format = st.selectbox("Choose cell format", list(cell_shapes.keys()))
cell_w, cell_h = cell_shapes[selected_format]

# Calculate how many fit
fit_cols = module_width // cell_w
fit_rows = module_height // cell_h
cell_count = fit_cols * fit_rows
used_area = cell_count * (cell_w * cell_h)
total_area = module_width * module_height
efficiency = used_area / total_area

# Generate Plotly figure
fig = go.Figure()

# Draw cells
for row in range(fit_rows):
    for col in range(fit_cols):
        x0 = col * cell_w
        y0 = row * cell_h
        fig.add_shape(
            type="rect",
            x0=x0, y0=y0, x1=x0 + cell_w, y1=y0 + cell_h,
            line=dict(color="black"),
            fillcolor="skyblue"
        )

# Outline the module box
fig.add_shape(
    type="rect",
    x0=0, y0=0, x1=module_width, y1=module_height,
    line=dict(color="black", width=3)
)

# Layout
fig.update_layout(
    width=600,
    height=400,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(showgrid=False, zeroline=False, range=[0, module_width]),
    yaxis=dict(showgrid=False, zeroline=False, range=[0, module_height]),
    plot_bgcolor='white'
)

# Show figure
st.plotly_chart(fig)

# Stats
st.markdown(f"**Cells packed:** {cell_count}")
st.markdown(f"**Packing efficiency:** {efficiency*100:.1f}% of module area")
st.caption("Visualized using Plotly for Streamlit Cloud compatibility.")
