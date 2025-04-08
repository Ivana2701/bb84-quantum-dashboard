import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import io

def bernstein_vazirani_circuit(secret_string):
    """Creates the Bernstein–Vazirani circuit for a given secret string."""
    n = len(secret_string)
    qc = QuantumCircuit(n + 1, n)

    # Initialize last qubit to |1⟩ and apply Hadamard to all
    qc.x(n)
    qc.h(range(n + 1))

    # Apply oracle U_f based on secret string
    for i, bit in enumerate(secret_string):
        if bit == "1":
            qc.cx(i, n)

    # Apply Hadamard to input register and measure
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def run_bv(secret_string):
    qc = bernstein_vazirani_circuit(secret_string)
    backend = AerSimulator()
    compiled = transpile(qc, backend)
    result = backend.run(compiled, shots=1024).result()
    counts = result.get_counts()
    return qc, counts

def render_bernstein():
    st.subheader("🧬 Bernstein–Vazirani Algorithm")
    st.markdown("""
    The Bernstein–Vazirani algorithm recovers a **hidden binary string** using just **one query**.

    This offers an exponential speedup over classical approaches which require multiple queries.
    """)

    secret_string = st.text_input("🔑 Enter a secret binary string:", value="1011")

    if not all(c in "01" for c in secret_string):
        st.error("Secret string must be composed only of 0s and 1s.")
        return

    if st.button("▶️ Run Bernstein–Vazirani Algorithm"):
        qc, counts = run_bv(secret_string)
        result_str = list(counts.keys())[0]

        st.success(f"✅ Recovered secret string: `{result_str}`")
        st.markdown("📊 **Measurement Counts:**")
        st.json(counts)

        st.subheader("🧠 Quantum Circuit")
        fig = qc.draw("mpl")
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)
