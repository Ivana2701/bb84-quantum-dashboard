import streamlit as st

# Algorithm module imports (to be implemented)
from components.algorithms.grover import render_grover
# from components.algorithms.qaoa import render_qaoa
# from components.algorithms.vqe import render_vqe
from components.algorithms.deutsch_jozsa import render_deutsch
from components.algorithms.bernstein_vazirani import render_bernstein

def render_tab6():
    st.header("🧪 Quantum Algorithms Lab")
    st.markdown("""
    Welcome to the Quantum Algorithms Lab!

    In this lab, you’ll experiment with powerful quantum algorithms that demonstrate how quantum computing goes beyond classical capabilities.

    🔍 **What’s inside:**
    - Run simulations of landmark quantum algorithms
    - Toggle between simulators and real IBM Quantum backends
    - See circuits, outputs, and how they apply to real-world problems
    """)

    st.markdown("## 🧠 Select an Algorithm to Explore")

    algo = st.selectbox(
        "Choose a quantum algorithm:",
        (
            "🔎 Grover’s Search",
            # "📦 QAOA (Optimization)",
            # "⚛️ VQE (Chemistry)",
            "🧮 Deutsch–Jozsa",
            "🧬 Bernstein–Vazirani"
        )
    )

    if "Grover" in algo:
        render_grover()
    # elif "QAOA" in algo:
    #     render_qaoa()
    # elif "VQE" in algo:
    #     render_vqe()
    elif "Deutsch" in algo:
        render_deutsch()
    elif "Bernstein" in algo:
        render_bernstein()
