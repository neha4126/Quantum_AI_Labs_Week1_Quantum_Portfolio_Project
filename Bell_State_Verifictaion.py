import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

sim = AerSimulator()

# 1. Define the 4 Bell states using plain text names
circuits = {
    "Phi_plus": QuantumCircuit(2, 2),
    "Phi_minus": QuantumCircuit(2, 2),
    "Psi_plus": QuantumCircuit(2, 2),
    "Psi_minus": QuantumCircuit(2, 2),
}

# Phi_plus: (|00> + |11>) / sqrt(2)
circuits["Phi_plus"].h(0)
circuits["Phi_plus"].cx(0, 1)

# Phi_minus: (|00> - |11>) / sqrt(2)
circuits["Phi_minus"].x(0)
circuits["Phi_minus"].h(0)
circuits["Phi_minus"].cx(0, 1)

# Psi_plus: (|01> + |10>) / sqrt(2)
circuits["Psi_plus"].x(1)
circuits["Psi_plus"].h(0)
circuits["Psi_plus"].cx(0, 1)

# Psi_minus: (|01> - |10>) / sqrt(2)
circuits["Psi_minus"].x(0)
circuits["Psi_minus"].x(1)
circuits["Psi_minus"].h(0)
circuits["Psi_minus"].cx(0, 1)

# 2. Measure, simulate (1024 shots), and print counts
for name, qc in circuits.items():
    qc.measure([0, 1], [0, 1])
    counts = sim.run(qc, shots=1024).result().get_counts()
    print(f"{name}: {counts}")
    plot_histogram(counts, title=name)

plt.show()