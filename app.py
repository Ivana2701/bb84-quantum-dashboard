import streamlit as st
import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import pandas as pd
import numpy as np

def create_bit_flow_table(result, eve_enabled):
    data = []

    for i in range(len(result["alice_bits"])):
        alice_bit = result["alice_bits"][i]
        alice_basis = result["alice_bases"][i]
        bob_basis = result["bob_bases"][i]
        bob_bit = result["bob_results"][i]

        if alice_basis == bob_basis:
            correct = "✅" if alice_bit == bob_bit else "❌"
        else:
            correct = "⚠️"  # basis mismatch

        row = {
            "Index": i,
            "Alice Bit": alice_bit,
            "Alice Basis": alice_basis,
            "Bob Basis": bob_basis,
            "Bob Bit": bob_bit,
            "Match?": correct
        }

        if eve_enabled:
            eve_basis = result["eve_bases"][i]
            row["Eve Basis"] = eve_basis

        data.append(row)

    return pd.DataFrame(data)


# Set up Streamlit page
st.set_page_config(page_title="Quantum Key Distribution", layout="wide")
st.title("🔐 Quantum Key Distribution vs Classical Cryptography")
if "bb84_with_eve" not in st.session_state:
    st.session_state.bb84_with_eve = None
if "bb84_without_eve" not in st.session_state:
    st.session_state.bb84_without_eve = None


# --- BB84 Helper Function ---
def run_circuit(qc, backend):
    qc = transpile(qc, backend)
    job = backend.run(qc, shots=1, memory=True)
    result = job.result()
    return int(result.get_memory()[0])

def bb84_simulation(n=20, eve_enabled=False):
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(n)]
    eve_bases = [random.choice(['+', 'x']) for _ in range(n)]
    bob_bases = [random.choice(['+', 'x']) for _ in range(n)]

    simulator = Aer.get_backend('aer_simulator')
    bob_results = []

    for i in range(n):
        qc = QuantumCircuit(1, 1)

        # Alice prepares qubit
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 'x':
            qc.h(0)

        # Eve intercepts
        if eve_enabled:
            if eve_bases[i] == 'x':
                qc.h(0)
            qc.measure(0, 0)
            eve_bit = run_circuit(qc, simulator)
            qc = QuantumCircuit(1, 1)
            if eve_bit == 1:
                qc.x(0)
            if eve_bases[i] == 'x':
                qc.h(0)

        # Bob measures
        if bob_bases[i] == 'x':
            qc.h(0)
        qc.measure(0, 0)
        bob_bit = run_circuit(qc, simulator)
        bob_results.append(bob_bit)

    # Key sifting (keep only matching bases)
    shared_bits_alice = []
    shared_bits_bob = []
    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            shared_bits_alice.append(alice_bits[i])
            shared_bits_bob.append(bob_results[i])

    # Error rate calculation
    errors = sum([a != b for a, b in zip(shared_bits_alice, shared_bits_bob)])
    error_rate = errors / len(shared_bits_alice) if shared_bits_alice else 0

    return {
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "eve_bases": eve_bases if eve_enabled else [''] * n,
        "shared_key_alice": shared_bits_alice,
        "shared_key_bob": shared_bits_bob,
        "error_rate": error_rate
    }

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🛰️ BB84 Protocol", "🧮 Classical Key Exchange", "📊 Comparison"])

# --- Tab 1: BB84 ---
with tab1:
    st.header("BB84 Quantum Key Distribution")
    st.write("Simulate Alice and Bob sharing a key using BB84, with or without eavesdropping.")

    st.subheader("Run BB84 Simulation")
    num_qubits = st.slider("Number of Qubits", 8, 100, 20)
    eve_enabled = st.toggle("Include Eve (eavesdropper)", value=False)

    if st.button("Run Simulation"):
        result = bb84_simulation(num_qubits, eve_enabled)

        if eve_enabled:
            st.session_state.bb84_with_eve = result
        else:
            st.session_state.bb84_without_eve = result
        
        st.markdown(f"**Error Rate:** {result['error_rate'] * 100:.2f}%")
        st.markdown(f"**Final Key (Alice):** {result['shared_key_alice']}")
        st.markdown(f"**Final Key (Bob):**   {result['shared_key_bob']}")
        
        st.subheader("Bit-by-Bit View")
        st.dataframe({
            "Alice Bit": result["alice_bits"],
            "Alice Basis": result["alice_bases"],
            "Bob Basis": result["bob_bases"],
            "Bob Result": result["bob_results"]
        })
        st.subheader("Visual Bit Flow (Alice → Eve → Bob)")
        flow_df = create_bit_flow_table(result, eve_enabled)
        st.dataframe(flow_df.style.applymap(
            lambda val: 'background-color: #d4edda' if val == '✅'
            else 'background-color: #f8d7da' if val == '❌'
            else 'background-color: #f0f0f0' if val == '⚠️'
            else ''
        ))

        

# --- Tab 2: Placeholder ---
with tab2:
    st.header("Classical Key Exchange (RSA)")
    st.write("Simulate Alice generating RSA keys and Bob sending her a secure message.")

    # Step 1: Generate RSA key pair for Alice
    if st.button("Generate RSA Keys"):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Serialize keys (to display)
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')

        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

        st.success("Keys generated for Alice!")
        st.code(pem_public, language='pem')

        # Step 2: Bob writes a message
        message = st.text_input("Bob's Message to Alice", value="Hello Alice! Quantum is cool.")
        if st.button("Encrypt and Send to Alice"):
            encrypted_message = public_key.encrypt(
                message.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            st.success("Message encrypted and sent to Alice.")
            st.code(encrypted_message.hex(), language='text')

            # Step 3: Alice decrypts it
            decrypted_message = private_key.decrypt(
                encrypted_message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()

            st.success("Alice decrypted the message successfully:")
            st.code(decrypted_message, language='text')

# --- Tab 3: Placeholder ---
with tab3:
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
