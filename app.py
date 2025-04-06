import streamlit as st
from components.tab1_bb84 import render_tab1
from components.tab2_rsa import render_tab2
from components.tab3_comparison import render_tab3
from components.tab4_shor import render_tab4

st.set_page_config(page_title="Quantum Key Distribution", layout="wide")

st.title("🔐 Quantum Key Distribution vs Classical Cryptography")

# Initialize state
if "bb84_with_eve" not in st.session_state:
    st.session_state.bb84_with_eve = None
if "bb84_without_eve" not in st.session_state:
    st.session_state.bb84_without_eve = None

# Tabs
tabs = st.tabs([
    "🛰️ BB84 Protocol",
    "🧮 Classical Key Exchange",
    "📊 Comparison",
    "💥 Quantum Attack (Shor's)"
])

with tabs[0]:
    render_tab1()
with tabs[1]:
    render_tab2()
with tabs[2]:
    render_tab3()
with tabs[3]:
    render_tab4()