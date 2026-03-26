import streamlit as st
import pandas as pd
from datetime import datetime, date

# Oldal konfiguráció - Modern, széles nézet
st.set_page_config(page_title="MindVault - Szerződéskezelő", layout="wide")

# --- STÍLUS (Hogy hasonlítson a képeidre) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_status_許可=True)

# --- MENÜ (Oldalsáv) ---
with st.sidebar:
    st.title("🛡️ MindVault")
    st.write("---")
    menu = st.radio("MENÜ", ["Vezérlőpult", "Alkalmazottak", "Beállítások"])
    st.write("---")
    st.caption("Bejelentkezve: Adminisztrátor")

# --- ADATOK KEZELÉSE ---
if 'employees' not in st.session_state:
    # Alap adatok a képeid alapján
    st.session_state.employees = [
        {"Név": "Kovács István", "Cég": "Tornyos Pékség Kft.", "Munkakör": "Pék", "Szerződés vége": "2024-03-27", "Orvosi": "2025-06-15", "Tüdőszűrés": "2025-08-20"},
        {"Név": "Farkas Tibor", "Cég": "Példa Bt.", "Munkakör": "Sofőr", "Szerződés vége": "2026-04-30", "Orvosi": "2025-03-25", "Tüdőszűrés": "2025-03-28"}
    ]

# Segédfüggvény a lejárat ellenőrzéséhez
def check_expiry(date_str):
    if not date_str or date_str == "HATÁROZATLAN": return "✅ Rendben"
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    diff = (d - date.today()).days
    if diff < 0: return "🔴 Lejárt"
    if diff <= 7: return "🟠 Sürgős"
    return "✅ Rendben"

# --- 1. VEZÉRLŐPULT NÉZET ---
if menu == "Vezérlőpult":
    st.header("Vezérlőpult")
    
    # Felső kártyák (mint a képeden)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Összes alkalmazott", len(st.session_state.employees))
    c2.metric("Lejár 30 napon belül", "0")
    c3.metric("Lejárt / Kritikus", "1", delta_color="inverse")
    c4.metric("Rendszer állapot", "Aktív")

    st.write("---")
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("📅 Havi Feladatterv")
        st.info("Minden rendben! Nincs közeli lejárat a következő 30 napban.")
    
    with col_side:
        st.subheader("📊 Gyors Statisztika")
        st.write("Kritikus (7 nap): 0")
        st.write("Sürgős (15 nap): 0")
        st.write("30 napon belül: 0")

# --- 2. ALKALMAZOTTAK NÉZET ---
elif menu == "Alkalmazottak":
    st.header("Alkalmazottak nyilvántartása")
    
    # Új rögzítése gomb
    with st.expander("➕ Új alkalmazott rögzítése"):
        with st.form("add_form"):
            col_a, col_b = st.columns(2)
            new_nev = col_a.text_input("Név")
            new_ceg = col_b.selectbox("Cég", ["Tornyos Pékség Kft.", "Példa Bt."])
            new_taj = col_a.text_input("TAJ-szám")
            new_ado = col_b.text_input("Adóazonosító")
            new_sz_veg = st.date_input("Szerződés vége", value=date.today())
            
            if st.form_submit_button("Mentés"):
                st.session_state.employees.append({
                    "Név": new_nev, "Cég": new_ceg, 
                    "Szerződés vége": str(new_sz_veg), 
                    "Orvosi": "2025-01-01", "Tüdőszűrés": "2025-01-01"
                })
                st.success("Alkalmazott rögzítve!")
                st.rerun()

    # Táblázat
    df = pd.DataFrame(st.session_state.employees)
    # Állapotok kiszámítása a megjelenítéshez
    df['Állapot'] = df['Szerződés vége'].apply(check_expiry)
    st.dataframe(df, use_container_width=True)

# --- 3. BEÁLLÍTÁSOK NÉZET ---
elif menu == "Beállítások":
    st.header("Rendszerbeállítások")
    
    st.subheader("🏢 Munkahelyek kezelése")
    st.text_input("Új munkahely neve", placeholder="pl. 11. sz. Bolt")
    st.button("Hozzáadás")
    
    st.subheader("📧 E-mail Konfiguráció")
    st.text_input("Küldő e-mail cím", "noreply@mindvault.hu")
    st.text_input("Értesítendő e-mail 1", "iroda@tornyospekseg.hu")
    st.button("Beállítások mentése")