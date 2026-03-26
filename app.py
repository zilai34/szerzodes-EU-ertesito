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

# Segédfüggvény a lejáratok színezéséhez a táblázatban
def check_expiry(date_val):
    try:
        if isinstance(date_val, str):
            d = datetime.strptime(date_val, "%Y-%m-%d").date()
        else:
            d = date_val
        diff = (d - date.today()).days
        if diff < 0: return "🔴 Lejárt"
        if diff <= 7: return "🟠 Sürgős"
        if diff <= 30: return "🟡 30 napon belül"
        return "✅ Rendben"
    except:
        return "❓ -"

# --- VEZÉRLŐPULT ---
if menu == "Vezérlőpult":
    st.header("Vezérlőpult")
    c1, c2, c3 = st.columns(3)
    c1.metric("Összes alkalmazott", len(st.session_state.employees))
    c2.metric("Rendszer állapot", "Aktív")
    
    st.write("---")
    st.subheader("🔔 Közelgő lejáratok (30 napon belül)")
    
    found_any = False
    for emp in st.session_state.employees:
        # 1. SZERZŐDÉS ELLENŐRZÉSE
        d_sz = datetime.strptime(emp['Szerződés vége'], "%Y-%m-%d").date()
        diff_sz = (d_sz - date.today()).days
        if 0 <= diff_sz <= 30:
            st.error(f"📄 **{emp['Név']}** munkaszerződése lejár **{diff_sz}** nap múlva! (Email: {emp['Email']})")
            found_any = True

        # 2. ORVOSI ELLENŐRZÉSE
        d_orv = datetime.strptime(emp['Orvosi lejárat'], "%Y-%m-%d").date()
        diff_orv = (d_orv - date.today()).days
        if 0 <= diff_orv <= 30:
            st.warning(f"⚕️ **{emp['Név']}** orvosi alkalmassága lejár **{diff_orv}** nap múlva! (Email: {emp['Email']})")
            found_any = True
            
        # 3. TÜDŐSZŰRŐ ELLENŐRZÉSE
        d_tud = datetime.strptime(emp['Tüdőszűrő lejárat'], "%Y-%m-%d").date()
        diff_tud = (d_tud - date.today()).days
        if 0 <= diff_tud <= 30:
            st.info(f"🫁 **{emp['Név']}** tüdőszűrője lejár **{diff_tud}** nap múlva! (Email: {emp['Email']})")
            found_any = True
    
    if not found_any:
        st.success("Nincs közeli lejárat a következő 30 napban.")

# --- ALKALMAZOTTAK NÉZET ---
elif menu == "Alkalmazottak":
    st.header("Alkalmazottak nyilvántartása")
    
    with st.expander("➕ Új alkalmazott rögzítése", expanded=True):
        with st.form("add_form"):
            col1, col2 = st.columns(2)
            nev = col1.text_input("Név")
            ceg = col2.selectbox("Cég", ["Tornyos Pékség Kft.", "DJ & K Bt.", "Egyéb"])
            
            col3, col4 = st.columns(2)
            sz_kezdete = col3.date_input("Szerződés kezdete", value=date.today())
            sz_vege = col4.date_input("Szerződés vége", value=date.today())
            
            alkalmassagi = st.date_input("Orvosi alkalmassági lejárat", value=date.today())
            tudoszuro = st.date_input("Tüdőszűrő lejárat", value=date.today())
            
            email = st.text_input("Alkalmazott e-mail címe (értesítésekhez)")
            
            if st.form_submit_button("Mentés"):
                if nev and email:
                    st.session_state.employees.append({
                        "Név": nev, 
                        "Cég": ceg, 
                        "Szerződés kezdete": str(sz_kezdete),
                        "Szerződés vége": str(sz_vege), 
                        "Orvosi lejárat": str(alkalmassagi),
                        "Tüdőszűrő lejárat": str(tudoszuro),
                        "Email": email
                    })
                    st.success(f"{nev} rögzítve!")
                    st.rerun()
                else:
                    st.error("A név és e-mail kitöltése kötelező!")

    if st.session_state.employees:
        df = pd.DataFrame(st.session_state.employees)
        st.subheader("Aktuális lista")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Még nincs rögzített alkalmazott.")

# --- BEÁLLÍTÁSOK ---
elif menu == "Beállítások":
    st.header("Beállítások")
    st.subheader("📧 Központi E-mail Konfiguráció")
    st.session_state.sender_email = st.text_input("Küldő e-mail cím", value="noreply@mindvault.hu")
    st.session_state.smtp_server = st.text_input("SMTP Szerver")
    st.session_state.smtp_pass = st.text_input("E-mail jelszó", type="password")
    
    if st.button("Mentés"):
        st.success("Beállítások elmentve!")
