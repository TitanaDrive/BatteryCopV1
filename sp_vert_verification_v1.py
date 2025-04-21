
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="SP-VERT: Chemistry Verification", layout="wide")

st.title("SP-VERT: Science Police Battery Verificator")
st.caption("Chemistry first. Format second. Truth always.")

# Step 1: Chemistry Selection
st.sidebar.header("1. Choose Chemistry")
cathode = st.sidebar.selectbox("Cathode", ["LFP", "NMC", "LMFP", "NCA"])
anode = st.sidebar.selectbox("Anode", ["Graphite", "Silicon", "LTO", "Li-metal"])

# Step 2: TRL
trl = st.sidebar.selectbox("2. TRL Level", ["Theoretical", "Lab", "Commercial"])

# Step 3: Energy Density
theoretical_ed = st.sidebar.number_input("Theoretical Energy Density (Wh/kg)", min_value=50.0, max_value=500.0, value=250.0)

# Step 4: Format
format_selected = st.sidebar.selectbox("3. Format", ["Blade", "Prismatic", "Pouch", "2170", "4680"])

# Chemistry–Format Compatibility Rules
allowed_combos = {
    ("LFP", "Graphite"): ["Blade", "Pouch", "Prismatic"],
    ("NMC", "Graphite"): ["Pouch", "Prismatic", "2170", "4680"],
    ("NMC", "Silicon"): ["2170", "4680", "Pouch"],
    ("NCA", "Graphite"): ["2170", "4680"],
    ("LFP", "LTO"): ["Prismatic", "Blade"],
}

# Check compatibility
valid_combo = (cathode, anode) in allowed_combos and format_selected in allowed_combos[(cathode, anode)]

# Display Inputs
st.markdown(f"### Input Summary")
st.write(f"- **Cathode:** {cathode}")
st.write(f"- **Anode:** {anode}")
st.write(f"- **TRL:** {trl}")
st.write(f"- **Theoretical Energy Density:** {theoretical_ed} Wh/kg")
st.write(f"- **Format:** {format_selected}")

# Verdict
if valid_combo:
    st.success("SP Verdict: Chemistry and format are realistic and compatible.")
    show_sim = True
else:
    st.error("SP Verdict: Format incompatible with selected chemistry. Simulation blocked.")
    show_sim = False

# Show simulation button if passed
if show_sim:
    if st.button("Simulate Electrochemistry (LFP|Graphite example)"):
        import pybamm
        model = pybamm.lithium_ion.DFN()
        param = pybamm.ParameterValues("Marquis2019")
        sim = pybamm.Simulation(model, parameter_values=param)
        sim.solve([0, 3600])
        time = sim.solution["Time [s]"].entries
        voltage = sim.solution["Terminal voltage [V]"].entries
        plt.figure(figsize=(8, 5))
        plt.plot(time / 60, voltage, label="Voltage", color="tab:red")
        plt.xlabel("Time [min]")
        plt.ylabel("Voltage [V]")
        plt.title("LFP|Graphite – 1C Discharge Simulation")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        st.pyplot(plt)
