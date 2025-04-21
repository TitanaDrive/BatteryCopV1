
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="SP-VERT Industrial Edition", layout="wide")
st.title("SP-VERT – Industrial Chemistry Verificator")
st.caption("Drop down into reality. Get punched by Science Police if you fake it.")

# Backend chemistry database (sample entries incl. Na-ion from Nature + Li-ion)
chemistry_data = {
    ("LFP", "Graphite"): {"theory_range": (100, 180), "formats": ["Blade", "Prismatic", "Pouch"]},
    ("NMC", "Graphite"): {"theory_range": (150, 250), "formats": ["Pouch", "Prismatic", "2170", "4680"]},
    ("NMC", "Silicon"): {"theory_range": (200, 300), "formats": ["Pouch", "2170", "4680"]},
    ("NCA", "Graphite"): {"theory_range": (180, 270), "formats": ["2170", "4680"]},
    ("LFP", "LTO"): {"theory_range": (60, 120), "formats": ["Prismatic", "Blade"]},
    ("Na-Mn", "HC"): {"theory_range": (80, 140), "formats": ["Prismatic", "Pouch"]},
    ("Na-Fe", "HC"): {"theory_range": (90, 160), "formats": ["Pouch", "Prismatic", "Blade"]}
}

# Step 1: Cathode and Anode Selection
st.sidebar.header("1. Select Your Chemistry")
all_cathodes = sorted(set([pair[0] for pair in chemistry_data.keys()]))
all_anodes = sorted(set([pair[1] for pair in chemistry_data.keys()]))

cathode = st.sidebar.selectbox("Cathode", all_cathodes)
anode = st.sidebar.selectbox("Anode", all_anodes)

# Step 2: Format and TRL
format_selected = st.sidebar.selectbox("Format", ["Blade", "Prismatic", "Pouch", "2170", "4680"])
trl = st.sidebar.selectbox("TRL Level", ["Theoretical", "Lab", "Commercial"])

# Step 3: Energy Densities
theoretical_ed = st.sidebar.number_input("Theoretical Energy Density (Wh/kg)", min_value=50.0, max_value=500.0, value=200.0)
lab_ed = st.sidebar.number_input("Lab/Measured Energy Density (Wh/kg)", min_value=0.0, max_value=500.0, value=0.0)

# Determine if chemistry is valid
combo_key = (cathode, anode)
valid_chem = combo_key in chemistry_data
if valid_chem:
    theory_min, theory_max = chemistry_data[combo_key]["theory_range"]
    valid_format = format_selected in chemistry_data[combo_key]["formats"]
else:
    valid_format = False
    theory_min, theory_max = 0, 0

# Display Inputs Summary
st.markdown("### Your Input Summary")
st.write(f"- **Cathode:** {cathode}")
st.write(f"- **Anode:** {anode}")
st.write(f"- **Format:** {format_selected}")
st.write(f"- **TRL:** {trl}")
st.write(f"- **Theoretical ED:** {theoretical_ed} Wh/kg")
st.write(f"- **Lab ED:** {lab_ed if lab_ed else 'N/A'}")

# SP Verdict Logic
if not valid_chem:
    st.error("SP Punch: This chemistry combo doesn’t exist in industrial reality. Back to school.")
elif not valid_format:
    st.error("SP Punch: This chemistry can’t be built in that format. Check your engineering!")
elif not (theory_min <= theoretical_ed <= theory_max):
    st.warning(f"SP Warning: Your theoretical ED is out of range for {cathode}+{anode}. Expected {theory_min}-{theory_max} Wh/kg.")
else:
    st.success("SP Verdict: Chemistry, format, and energy density are realistic.")

    if st.button("Pack It! Show Tetris"):
        # Tetris Visualizer
        st.markdown("### Battery Tetris – Pack Like a Pro")
        module_w, module_h = 10, 6
        cell_shapes = {
            "Blade": {"w": 2.5, "h": 0.5, "color": "#D3E4CD"},
            "Prismatic": {"w": 2.2, "h": 1.2, "color": "#FFC898"},
            "Pouch": {"w": 2.0, "h": 0.8, "color": "#AEDFF7"},
            "2170": {"w": 1.0, "h": 1.0, "color": "#F6C6EA"},
            "4680": {"w": 2.0, "h": 2.0, "color": "#C8A2C8"},
        }

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
        box_area = module_w * module_h
        cell_area = cw * ch
        filled_area = count * cell_area
        efficiency = (filled_area / box_area) * 100

        st.pyplot(fig)
        st.markdown(f"**Packing Efficiency:** {efficiency:.1f}% with {count} cells")
        st.caption("SP Verdict: This pack is tight.")
