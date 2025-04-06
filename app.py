import streamlit as st
from components.tab1_bb84 import render_tab1
from components.tab2_rsa import render_tab2
from components.tab3_comparison import render_tab3

st.set_page_config(page_title="Quantum Key Distribution", layout="wide")

st.title("🔐 Quantum Key Distribution vs Classical Cryptography")

if "bb84_with_eve" not in st.session_state:
    st.session_state.bb84_with_eve = None
if "bb84_without_eve" not in st.session_state:
    st.session_state.bb84_without_eve = None

tab1, tab2, tab3 = st.tabs(["🛰️ BB84 Protocol", "🧮 Classical Key Exchange", "📊 Comparison"])

with tab1:
    render_tab1()

with tab2:
    render_tab2()

with tab3:
    render_tab3()
