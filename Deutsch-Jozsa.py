import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def create_constant_oracle(n: int) -> QuantumCircuit:
    """Creates a constant oracle (outputs either always 0 or always 1)."""
    oracle = QuantumCircuit(n + 1, name="Constant Oracle")
    # Randomly choose between f(x)=0 (no op) or f(x)=1 (flip ancilla)
    if np.random.randint(2) == 1:
        oracle.x(n)
    return oracle

def create_balanced_oracle(n: int) -> QuantumCircuit:
    """Creates a balanced oracle (outputs 1 for exactly half of the inputs)."""
    oracle = QuantumCircuit(n + 1, name="Balanced Oracle")
    bitmask = np.random.randint(0, 2, size=n)
    for i in range(n):
        if bitmask[i] == 1:
            oracle.x(i)
    for i in range(n):
        oracle.cx(i, n)
    for i in range(n):
        if bitmask[i] == 1:
            oracle.x(i)
    return oracle

def run_deutsch_jozsa_verification(oracle: QuantumCircuit, n: int, oracle_name: str, shots: int = 1024):
    print(f"==================================================")
    print(f"          VERIFYING: {oracle_name.upper()}")
    print(f"==================================================")
    
    # --- 1. Initial Probabilities (Before Oracle / Superposition stage) ---
    # After applying H gates to |0>^n |1>, every input qubit is in an equal superposition
    # of |0> and |1> with probability 0.5 each.
    print("\n--- 1. Initial Qubit Probabilities (Post-Hadamard Superposition) ---")
    for i in range(n):
        print(f"Qubit {i}: P(0) = 0.5000 | P(1) = 0.5000")

    # --- Build Algorithm Circuit ---
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    # Run simulation
    backend = AerSimulator()
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Calculate modified individual qubit probabilities from measurement counts
    single_qubit_zeros = [0] * n
    single_qubit_ones = [0] * n

    for bitstring, count in counts.items():
        reversed_bits = bitstring[::-1]
        for i, bit in enumerate(reversed_bits):
            if bit == '0':
                single_qubit_zeros[i] += count
            else:
                single_qubit_ones[i] += count

    # --- 2. Modified Probabilities (After Oracle and Interference) ---
    print("\n--- 2. Modified Qubit Probabilities (Post-Interference & Measurement) ---")
    for i in range(n):
        p_zero = single_qubit_zeros[i] / shots
        p_one = single_qubit_ones[i] / shots
        print(f"Qubit {i}: P(0) = {p_zero:.4f} | P(1) = {p_one:.4f}")

    # Final Verdict
    all_zeros = "0" * n
    is_constant = all_zeros in counts and counts[all_zeros] == shots
    conclusion = "Constant" if is_constant else "Balanced"
    
    print(f"\nMeasured Bitstring Counts: {counts}")
    print(f"Algorithm Verdict: The function is {conclusion}\n")

def main():
    n = 4  # Number of input qubits

    # Define the two required oracle functions
    oracle_const = create_constant_oracle(n)
    oracle_bal = create_balanced_oracle(n)

    # Check and display results for both oracles
    run_deutsch_jozsa_verification(oracle_const, n, oracle_name="Oracle 1 (Constant)")
    run_deutsch_jozsa_verification(oracle_bal, n, oracle_name="Oracle 2 (Balanced)")

if __name__ == "__main__":
    main()
    