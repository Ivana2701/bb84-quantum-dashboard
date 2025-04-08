import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import io
import numpy as np


def grover_oracle(target: str):
    """Constructs a Grover oracle for a given target bitstring."""
    n = len(target)
    oracle = QuantumCircuit(n)
    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            oracle.x(i)
    oracle.h(n - 1)
    oracle.mcx(list(range(n - 1)), n - 1)
    oracle.h(n - 1)
    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            oracle.x(i)
    return oracle


def grover_diffuser(n):
    """Creates a Grover diffuser circuit for n qubits."""
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def grover_circuit(target_string):
    n = len(target_string)
    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    oracle = grover_oracle(target_string)
    diffuser = grover_diffuser(n)

    qc.compose(oracle, inplace=True)
    qc.compose(diffuser, inplace=True)
    qc.measure(range(n), range(n))

    return qc


def run_grover(target_string):
    qc = grover_circuit(target_string)
    backend = AerSimulator()
    compiled = transpile(qc, backend)
    result = backend.run(compiled, shots=1024).result()
    counts = result.get_counts()
    return qc, counts


def render_grover():
    st.subheader("🔍 Grover's Algorithm – Search with a Quantum Speedup")
    st.markdown("""
    Grover's algorithm finds a **marked item** in an unsorted database in roughly √N time.  
    It’s useful for search problems and optimization.

    We’ll look for a **target bitstring**, for example: `101`
    """)

    target = st.text_input("🎯 Enter target bitstring:", value="101")
    if not all(c in "01" for c in target):
        st.error("Bitstring must be binary.")
        return

    if st.button("▶️ Run Grover’s Algorithm"):
        with st.spinner("Running Grover's Algorithm..."):
            qc, counts = run_grover(target)
            most_common = max(counts, key=counts.get)

            st.success(f"Most likely result: `{most_common}`")
            st.markdown("📊 **Measurement Histogram**")
            st.pyplot(plot_histogram(counts, figsize=(7, 4)))

            if st.checkbox("🧠 Show Quantum Circuit"):
                fig = qc.draw("mpl")
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.image(buf)
