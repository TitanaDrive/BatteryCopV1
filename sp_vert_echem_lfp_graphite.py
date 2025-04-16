
import pybamm
import matplotlib.pyplot as plt

# Initialize model: Doyle-Fuller-Newman model (accurate and realistic)
model = pybamm.lithium_ion.DFN()

# Load validated industrial parameter set for LFP|Graphite
param = pybamm.ParameterValues("Marquis2019")

# Setup and solve for 1-hour discharge (3600 seconds)
sim = pybamm.Simulation(model, parameter_values=param)
sim.solve([0, 3600])

# Plot key results
sim.plot(["Terminal voltage [V]", "Discharge capacity [A.h]"])
