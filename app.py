import streamlit as st
import pandas as pd
from datetime import datetime, date

# Oldal beállítása
st.set_page_config(page_title="MindVault - Szerződéskezelő", layout="wide")

# --- STÍLUS BEÁLLÍTÁSA ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { 
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        border: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENÜ (Oldalsáv) ---
with st.sidebar:
    st.title("🛡️ MindVault")
    st.write("---")
    menu = st.radio("MENÜ", ["Vezérlőpult", "Alkalmazottak", "Beállítások"])
    st.write("---")
    st.caption("Bejelentkezve: Adminisztrátor")

# --- ADATOK (Minta) ---
if 'employees' not in st.session_state:
    st.session_state.employees = [
        {"Név": "Kovács István", "Cég": "Tornyos Pékség Kft.", "Szerződés vége": "2026-03-27", "Orvosi": "2025-06-15"},
        {"Név": "Farkas Tibor", "Cég": "Példa Bt.", "Szerződés vége": "2026-04-30", "Orvosi": "2025-03-25"}
    ]

# Segédfüggvény az állapothoz
def check_expiry(date_val):
    try:
        if isinstance(date_val, str):
            d = datetime.strptime(date_val, "%Y-%m-%d").date()
        else:
            d = date_val
        diff = (d - date.today()).days
        if diff < 0: return "🔴 Lejárt"
        if diff <= 7: return "🟠 Sürgős"
        return "✅ Rendben"
    except:
        return "❓ Ismeretlen"

# --- OLDALAK ---
if menu == "Vezérlőpult":
    st.header("Vezérlőpult")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Összes alkalmazott", len(st.session_state.employees))
    c2.metric("Lejár 30 napon belül", "0")
    c3.metric("Lejárt / Kritikus", "0")
    c4.metric("Rendszer állapot", "Aktív")
    
    st.write("---")
    st.subheader("📅 Havi Feladatterv")
    st.info("Minden rendben! Nincs közeli lejárat a következő 30 napban.")

elif menu == "Alkalmazottak":
    st.header("Alkalmazottak nyilvántartása")
    
    with st.expander("➕ Új alkalmazott rögzítése"):
        with st.form("add_form"):
            c_a, c_b = st.columns(2)
            n_nev = c_a.text_input("Név")
            n_ceg = c_b.selectbox("Cég", ["Tornyos Pékség Kft.", "Példa Bt."])
            n_veg = st.date_input("Szerződés vége")
            if st.form_submit_button("Mentés"):
                st.session_state.employees.append({"Név": n_nev, "Cég": n_ceg, "Szerződés vége": str(n_veg), "Orvosi": "2025-01-01"})
                st.rerun()

    df = pd.DataFrame(st.session_state.employees)
    df['Állapot'] = df['Szerződés vége'].apply(check_expiry)
    st.dataframe(df, use_container_width=True)

elif menu == "Beállítások":
    st.header("Rendszerbeállítások")
    st.subheader("📧 E-mail Konfiguráció")
    st.text_input("Küldő e-mail cím", "noreply@mindvault.hu")
    st.button("Mentés")
