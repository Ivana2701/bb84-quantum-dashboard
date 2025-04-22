from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def render_tab5():
    st.header("🚨 Harvest Now, Decrypt Later")
    st.markdown("""
    Quantum computers are coming. Some adversaries are already collecting encrypted data now—
    with plans to decrypt it **later** once quantum computers are powerful enough.

    This is called **"Harvest Now, Decrypt Later"**.

    🔒 Today’s encryption (like RSA) is safe **now** — but will be broken **later** by Shor’s algorithm.
    📦 So attackers can store encrypted data today and decrypt it in the quantum future.
    """)

    year_range = st.slider("Select Time Range", 2024, 2040, (2024, 2040))
    years = np.arange(year_range[0], year_range[1] + 1)
    rsa_security = np.linspace(1.0, 0.1, len(years))
    pqc_security = np.full_like(rsa_security, 1.0)


    fig, ax = plt.subplots()
    ax.plot(years, rsa_security, label="RSA Security", linestyle="--", linewidth=2)
    ax.plot(years, pqc_security, label="Post-Quantum Crypto (PQC)", linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("Relative Security")
    ax.set_title("Projected Security of RSA vs PQC")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    st.subheader("🔐 What is Post-Quantum Cryptography (PQC)?")
    st.markdown("""
    | Algorithm   | Type            | Purpose              | NIST Status | Notes                             |
    |-------------|------------------|-----------------------|-------------|-----------------------------------|
    | **Kyber**   | Lattice-based   | Encryption (KEM)      | ✅ Standard | Secure key exchange               |
    | **Dilithium** | Lattice-based | Digital Signatures    | ✅ Standard | Efficient, robust                 |
    | **Falcon**  | Lattice-based   | Digital Signatures    | ✅ Standard | Compact, efficient, more complex  |
    """)

    st.subheader("✅ Future-Proofing Checklist")
    st.checkbox("🔐 Use PQC algorithms (Kyber, Dilithium, Falcon)", value=True)
    st.checkbox("🛰️ Use BB84 for secure key exchange", value=True)
    st.checkbox("💾 Store sensitive encrypted data securely", value=False)
    st.checkbox("📡 Monitor quantum advancements & upgrade protocols", value=False)

    st.subheader("🤝 BB84 + PQC = Quantum-Safe Security Stack")
    st.markdown("""
    - **BB84** handles the key exchange securely using quantum mechanics (detects interception).
    - **PQC** handles encryption and signing, even on classical hardware.

    Together, they ensure:
    ✅ Keys are safely exchanged (BB84)  
    ✅ Messages are securely encrypted (Kyber)  
    ✅ Integrity is preserved with signatures (Dilithium/Falcon)
    """)

    st.info("🔭 Want to try post-quantum + quantum key experiments with IBM Quantum? Just toggle backend in Shor tab.")

