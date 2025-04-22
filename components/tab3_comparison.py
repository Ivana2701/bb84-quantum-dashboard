import streamlit as st
import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import pandas as pd
import numpy as np

# Import the missing function from helpers
from components.helpers import create_bit_flow_table

def render_tab3():
    st.header("📊 Quantum vs Classical Comparison")

    st.subheader("1. BB84 Error Rate Comparison")
    with_eve = st.session_state.get("bb84_with_eve")
    without_eve = st.session_state.get("bb84_without_eve")

    if with_eve and without_eve:
        error_data = {
            "Scenario": ["BB84 Without Eve", "BB84 With Eve"],
            "Error Rate (%)": [
                without_eve["error_rate"] * 100,
                with_eve["error_rate"] * 100
            ]
        }
        chart_df = pd.DataFrame(error_data)
        st.bar_chart(chart_df.set_index("Scenario"))
    else:
        st.warning("Run BB84 both with and without Eve to compare error rates.")

    st.subheader("2. Feature Comparison Table")
    comparison_table = pd.DataFrame({
        "Feature": [
            "Key Exchange Method",
            "Eavesdropper Detection",
            "Requires Quantum Channel",
            "Security (Post-Quantum)",
            "Key Length Flexibility",
            "Public/Private Keys",
        ],
        "BB84 (Quantum)": [
            "Quantum Bit Exchange",
            "✅ Yes (via error rate)",
            "✅ Yes",
            "✅ Quantum-safe",
            "Depends on basis matches",
            "❌ No (symmetric)"
        ],
        "RSA (Classical)": [
            "Mathematical Encryption",
            "❌ No",
            "❌ No",
            "❌ Breakable by quantum",
            "Fixed (e.g., 2048-bit)",
            "✅ Yes (public/private)"
        ]
    })
    st.dataframe(comparison_table)

    st.subheader("3. Export BB84 Data to CSV")

    if with_eve or without_eve:
        option = st.radio("Select key to export:", ["BB84 Without Eve", "BB84 With Eve"])
        data = without_eve if option == "BB84 Without Eve" else with_eve

        data_ready = (without_eve if option == "BB84 Without Eve" else with_eve) is not None

        st.download_button(
            label="Download Bit Flow Table as CSV",
            disabled=not data_ready,
            data=(
                create_bit_flow_table(
                    without_eve if option == "BB84 Without Eve" else with_eve,
                    eve_enabled=(option == "BB84 With Eve")
                ).to_csv(index=False).encode('utf-8') if data_ready else None
            ),
            file_name=f'{option.lower().replace(" ", "_")}_bitflow.csv',
            mime='text/csv',
        )

        if not data_ready:
            st.info(f"Run the BB84 simulation for **{option}** to enable export.")

    else:
        st.info("Run a BB84 simulation first to enable CSV export.")
