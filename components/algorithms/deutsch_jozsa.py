import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import io


def deutsch_jozsa_oracle(case='constant'):
    """Create Deutsch–Jozsa oracle circuit for f(x)."""
    oracle = QuantumCircuit(2)
    if case == 'balanced':
        oracle.cx(0, 1)  # f(x) = x
    elif case == 'constant':
        oracle.i(0)  # f(x) = 0 (or you can flip with X for f(x)=1)
    return oracle


def run_deutsch_jozsa(oracle_type):
    qc = QuantumCircuit(2, 1)

    # Step 1: Initialize
    qc.x(1)
    qc.h([0, 1])

    # Step 2: Oracle
    oracle = deutsch_jozsa_oracle(oracle_type)
    qc.compose(oracle, inplace=True)

    # Step 3: Final Hadamard and Measure
    qc.h(0)
    qc.measure(0, 0)

    backend = AerSimulator()
    compiled = transpile(qc, backend)
    result = backend.run(compiled, shots=1024).result()
    counts = result.get_counts()
    return qc, counts


def render_deutsch():
    st.subheader("🧮 Deutsch–Jozsa Algorithm")
    st.markdown("""
    Determines if a function `f(x)` is **constant** or **balanced** with just **one query**.
    
    Try simulating a black-box oracle to see how quantum speedup works!
    """)

    oracle_type = st.radio("Choose Oracle Type (f(x))", ["constant", "balanced"])

    if st.button("▶️ Run Deutsch–Jozsa Algorithm"):
        qc, counts = run_deutsch_jozsa(oracle_type)
        measured_bit = list(counts.keys())[0]

        st.success(f"✅ Result: `{measured_bit}` → Function is **{oracle_type}**")
        st.markdown("📊 **Measurement Counts:**")
        st.json(counts)

        st.subheader("🧠 Quantum Circuit")
        fig = qc.draw("mpl")
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)
