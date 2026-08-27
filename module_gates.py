"""
Quantum Gate Playground Module
==============================
A lightweight library of reusable single- and multi-qubit unitary quantum gates
with circuit diagrams and statevector inspection utilities built on Qiskit 1.0+.
"""

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


# ==============================================================================
# Visualization Utility
# ==============================================================================
def print_statevector(sv: Statevector, qc: QuantumCircuit = None, label: str = ""):
    """
    Displays the circuit diagram, mathematical Dirac representation, 
    numerical amplitudes, and measurement probabilities.
    """
    if label:
        print(f"--- {label} ---")
    
    if qc is not None:
        print("Circuit Diagram:")
        print(qc.draw("text"))
        print()

    print(f"Dirac Notation :\n{sv.draw('text')}")
    print(f"Amplitudes     : {sv.data.round(4)}")
    print(f"Probabilities  : {sv.probabilities_dict(decimals=4)}\n")


# ==============================================================================
# Single-Qubit Unitary Gates
# ==============================================================================
def apply_x(initial_state: str = "0", show_circuit: bool = True) -> Statevector:
    """
    Applies the Pauli-X (NOT / Bit-Flip) gate to a 1-qubit basis state.
    Transforms |0> -> |1> and |1> -> |0>.
    """
    sv = Statevector.from_label(initial_state)
    qc = QuantumCircuit(1)
    qc.x(0)
    
    if show_circuit:
        print(f"[Pauli-X Circuit for initial state |{initial_state}>]")
        print(qc.draw("text"))
        print()
        
    return sv.evolve(qc)


def apply_z(initial_state: str = "0", show_circuit: bool = True) -> Statevector:
    """
    Applies the Pauli-Z (Phase-Flip) gate to a 1-qubit basis state.
    Leaves |0> invariant and maps |1> -> -|1>.
    """
    sv = Statevector.from_label(initial_state)
    qc = QuantumCircuit(1)
    qc.z(0)
    
    if show_circuit:
        print(f"[Pauli-Z Circuit for initial state |{initial_state}>]")
        print(qc.draw("text"))
        print()
        
    return sv.evolve(qc)


def apply_h(initial_state: str = "0", show_circuit: bool = True) -> Statevector:
    """
    Applies the Hadamard (H) gate to create an equal superposition.
    Transforms |0> -> |+> and |1> -> |->.
    """
    sv = Statevector.from_label(initial_state)
    qc = QuantumCircuit(1)
    qc.h(0)
    
    if show_circuit:
        print(f"[Hadamard Circuit for initial state |{initial_state}>]")
        print(qc.draw("text"))
        print()
        
    return sv.evolve(qc)


# ==============================================================================
# Multi-Qubit Controlled Gates
# ==============================================================================
def apply_cnot(initial_state: str = "00", control: int = 0, target: int = 1, show_circuit: bool = True) -> Statevector:
    """
    Applies the Controlled-NOT (CX) gate across a 2-qubit system.
    Flips the target qubit if and only if the control qubit is in state |1>.
    """
    sv = Statevector.from_label(initial_state)
    qc = QuantumCircuit(2)
    qc.cx(control, target)
    
    if show_circuit:
        print(f"[CNOT Circuit for initial state |{initial_state}> (ctrl=q{control}, tgt=q{target})]")
        print(qc.draw("text"))
        print()
        
    return sv.evolve(qc)


def apply_toffoli(initial_state: str = "000", c1: int = 0, c2: int = 1, target: int = 2, show_circuit: bool = True) -> Statevector:
    """
    Applies the Toffoli (CCX / Controlled-Controlled-NOT) gate across 3 qubits.
    Flips the target qubit if and only if both control qubits are in state |1>.
    """
    sv = Statevector.from_label(initial_state)
    qc = QuantumCircuit(3)
    qc.ccx(c1, c2, target)
    
    if show_circuit:
        print(f"[Toffoli Circuit for initial state |{initial_state}> (ctrl=q{c1},q{c2}, tgt=q{target})]")
        print(qc.draw("text"))
        print()
        
    return sv.evolve(qc)