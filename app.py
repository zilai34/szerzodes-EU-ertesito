import streamlit as st
import pandas as pd
from datetime import datetime, date

# Oldal konfiguráció
st.set_page_config(page_title="MindVault - Szerződéskezelő", layout="wide")

# --- STÍLUS ---
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

# --- MENÜ ---
with st.sidebar:
    st.title("🛡️ MindVault")
    st.write("---")
    menu = st.radio("MENÜ", ["Vezérlőpult", "Alkalmazottak", "Beállítások"])
    st.write("---")
    st.caption("Bejelentkezve: Adminisztrátor")

# --- ADATOK KEZELÉSE ---
if 'employees' not in st.session_state:
    st.session_state.employees = []

# Segédfüggvény a lejáratok színezéséhez
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
        return "❓ -"

# --- ALKALMAZOTTAK NÉZET ---
if menu == "Alkalmazottak":
    st.header("Alkalmazottak nyilvántartása")
    
    with st.expander("➕ Új alkalmazott rögzítése", expanded=True):
        with st.form("add_form"):
            # 1. SOR: Név és Cég
            col1, col2 = st.columns(2)
            nev = col1.text_input("Név")
            ceg = col2.selectbox("Cég", ["Tornyos Pékség Kft.", "Példa Bt.", "Egyéb"])
            
            # 2. SOR: Szerződés kezdete és vége
            col3, col4 = st.columns(2)
            sz_kezdete = col3.date_input("Szerződés kezdete", value=date.today())
            sz_vege = col4.date_input("Szerződés vége", value=date.today())
            
            # 3. SOR: Alkalmassági (külön sor)
            alkalmassagi = st.date_input("Orvosi alkalmassági lejárat", value=date.today())
            
            # 4. SOR: Tüdőszűrő (külön sor)
            tudoszuro = st.date_input("Tüdőszűrő lejárat", value=date.today())
            
            # Mentés gomb
            if st.form_submit_button("Mentés"):
                if nev:
                    st.session_state.employees.append({
                        "Név": nev, 
                        "Cég": ceg, 
                        "Szerződés kezdete": str(sz_kezdete),
                        "Szerződés vége": str(sz_vege), 
                        "Orvosi lejárat": str(alkalmassagi),
                        "Tüdőszűrő lejárat": str(tudoszuro)
                    })
                    st.success(f"{nev} rögzítve!")
                    st.rerun()
                else:
                    st.error("A név kitöltése kötelező!")

    # Táblázat megjelenítése
    if st.session_state.employees:
        df = pd.DataFrame(st.session_state.employees)
        
        # Állapot oszlopok hozzáadása a figyelmeztetésekhez
        df['Szerződés állapota'] = df['Szerződés vége'].apply(check_expiry)
        df['Orvosi állapota'] = df['Orvosi lejárat'].apply(check_expiry)
        
        st.subheader("Aktuális lista")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Még nincs rögzített alkalmazott.")

# --- VEZÉRLŐPULT ---
elif menu == "Vezérlőpult":
    st.header("Vezérlőpult")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Összes alkalmazott", len(st
