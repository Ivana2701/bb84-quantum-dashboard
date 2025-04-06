import streamlit as st
from components.helpers import bb84_simulation, create_bit_flow_table

def render_tab1():
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
        st.dataframe(flow_df.style.map(
            lambda val: 'background-color: #d4edda' if val == '✅'
            else 'background-color: #f8d7da' if val == '❌'
            else 'background-color: #f0f0f0' if val == '⚠️'
            else ''
        ))
