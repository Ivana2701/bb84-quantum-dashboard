import streamlit as st
import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import pandas as pd
import numpy as np
def render_tab2():
    st.header("Classical Key Exchange (RSA)")
    st.write("Simulate Alice generating RSA keys and Bob sending her a secure message.")

    with st.expander("🔍 What is RSA?"):
        st.markdown("""
        RSA is a classical cryptographic algorithm used in secure messaging, websites (HTTPS), and digital signatures.

        - **Alice** generates a public/private key pair.
        - **Bob** encrypts a message using **Alice’s public key**.
        - Only **Alice’s private key** can decrypt it.
        - Eve can intercept the message but **cannot decrypt it** without the private key.
        """)

    with st.expander("⚠️ Why compare with BB84?"):
        st.markdown("""
        - RSA **does not detect eavesdropping** — if Eve copies the message, you'll never know.
        - RSA is **mathematically secure**, but **can be broken** by quantum computers using **Shor’s algorithm**.
        - BB84, on the other hand, uses **quantum mechanics** to detect any interception.
        """)

    if st.button("Generate RSA Keys"):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

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
