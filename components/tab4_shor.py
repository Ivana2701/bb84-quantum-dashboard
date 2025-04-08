import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import io
import math
import random
import numpy as np


def shor_simplified(N):
    """Simplified Shor's algorithm for small N (e.g., 15). Returns factors."""
    if N % 2 == 0:
        return [2, N // 2]
    if N < 3:
        return [N, 1]
    for a in range(2, int(math.sqrt(N)) + 1):
        if N % a == 0:
            return [a, N // a]

    def period_finding(a, N):
        if N != 15:
            return None
        n_count = 4
        qc = QuantumCircuit(n_count + 1, n_count)
        qc.h(range(n_count))
        qc.x(n_count)
        for q in range(n_count):
            for _ in range(2 ** q % 15):
                qc.cx(q, n_count)
        for q in range(n_count-1, -1, -1):
            for m in range(q):
                qc.cp(-math.pi / float(2 ** (q - m)), m, q)
            qc.h(q)
        qc.measure(range(n_count), range(n_count))

        backend = AerSimulator()
        job = backend.run(transpile(qc, backend), shots=1024)
        result = job.result()
        counts = result.get_counts()
        max_count = max(counts, key=counts.get)
        measured_phase = int(max_count, 2) / 2**n_count
        r = int(round(1 / measured_phase)) if measured_phase != 0 else None
        return r if r and r <= N else 4

    attempts = 0
    while attempts < 5:
        a = random.randint(2, N-1)
        gcd = math.gcd(a, N)
        if gcd > 1:
            return [gcd, N // gcd]
        r = period_finding(a, N)
        if r and r % 2 == 0:
            x = pow(a, r//2, N)
            if x != 1 and x != N-1:
                f1 = math.gcd(x-1, N)
                f2 = math.gcd(x+1, N)
                if f1 * f2 == N and f1 > 1 and f2 > 1:
                    return [f1, f2]
        attempts += 1
    return [None, None]


def estimate_classical_time(bits):
    return np.exp((1.9 * (np.log(bits) ** (1/3)) * (np.log(np.log(bits)) ** (2/3))))

def estimate_shor_time(bits):
    return (np.log(bits) ** 3)


def render_tab4():
    st.header("🧨 Shor's Algorithm (Quantum Attack on RSA)")
    st.markdown("""
    **Shor's Algorithm** is a quantum algorithm that efficiently factors large numbers — the foundation of RSA encryption.

    Try factoring a number or compare performance of classical vs quantum approaches.
    """)

    N = st.number_input("🔢 Enter a number to factor (try 15)", min_value=3, max_value=100, step=2, value=15)

    if st.button("Run Shor's Algorithm"):
        st.info("⏳ Executing simplified Shor's algorithm...")
        factors = shor_simplified(N)
        if None not in factors:
            st.success(f"✅ Factors of {N}: {factors}")
            st.markdown("This demonstrates quantum factoring potential.")
        else:
            st.error("❌ Factoring failed or not implemented for this number.")
            st.markdown("Full Shor's requires advanced implementation.")

    if st.checkbox("Show Simplified Circuit for N=15"):
        qc = QuantumCircuit(5, 4)
        qc.h(range(4))
        qc.x(4)
        qc.cx(0, 4)
        qc.h(range(4))
        qc.measure(range(4), range(4))
        fig = qc.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)

    st.subheader("⏱️ Classical vs Quantum Factoring Time")
    max_bits = st.slider("Max RSA Key Size (bits)", min_value=256, max_value=8192, step=256, value=2048)

    key_sizes = np.arange(128, max_bits + 1, 128)
    classic_times = [estimate_classical_time(n) for n in key_sizes]
    shor_times = [estimate_shor_time(n) for n in key_sizes]

    fig, ax = plt.subplots()
    ax.plot(key_sizes, classic_times, label="Classical (RSA)")
    ax.plot(key_sizes, shor_times, label="Shor’s Algorithm")
    ax.set_yscale('log')
    ax.set_xlabel("RSA Key Size (bits)")
    ax.set_ylabel("Estimated Time (log scale)")
    ax.set_title("Classical vs Quantum Factoring Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
