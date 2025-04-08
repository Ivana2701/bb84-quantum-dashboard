import streamlit as st
from components.tab1_bb84 import render_tab1
from components.tab2_rsa import render_tab2
from components.tab3_comparison import render_tab3
from components.tab4_shor import render_tab4
from components.tab5_future_threat import render_tab5
from components.tab6_algorithms import render_tab6


st.set_page_config(page_title="Quantum Key Distribution", layout="wide")

st.title("🔐 Quantum Key Distribution vs Classical Cryptography")

# Initialize state
if "bb84_with_eve" not in st.session_state:
    st.session_state.bb84_with_eve = None
if "bb84_without_eve" not in st.session_state:
    st.session_state.bb84_without_eve = None

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🛰️ BB84 Protocol",
    "🧮 Classical Key Exchange",
    "📊 Comparison",
    "💥 Quantum Attack (Shor's)",
    "🔮 Future Threats (PQC)",
     "🧪 Quantum Algorithms Lab"

])

with tab1:
    render_tab1()

with tab2:
    render_tab2()

with tab3:
    render_tab3()

with tab4:
    render_tab4()

with tab5:
    render_tab5()

with tab6:
    render_tab6()
