import streamlit as st
import pandas as pd
from datetime import datetime, date

# Oldal konfiguráció
st.set_page_config(page_title="MindVault - Szerződéskezelő", layout="wide")

# --- ADATOK KEZELÉSE ---
if 'employees' not in st.session_state:
    st.session_state.employees = []

# Admin e-mail címek alapértelmezett értékei
if 'admin_email_1' not in st.session_state:
    st.session_state.admin_email_1 = "iroda@tornyospekseg.hu"
if 'admin_email_2' not in st.session_state:
    st.session_state.admin_email_2 = "management@tornyospekseg.hu"

# Segédfüggvény a napok kiszámításához
def get_diff(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (d - date.today()).days
    except:
        return 999

# --- MENÜ ---
with st.sidebar:
    st.title("🛡️ MindVault")
    menu = st.radio("MENÜ", ["Vezérlőpult", "Alkalmazottak", "Beállítások"])
    st.write("---")
    st.caption("Bejelentkezve: Adminisztrátor")

# --- VEZÉRLŐPULT ---
if menu == "Vezérlőpult":
    st.header("📊 Vezérlőpult")
    c1, c2 = st.columns(2)
    c1.metric("Összes alkalmazott", len(st.session_state.employees))
    c2.metric("Rendszer állapot", "Aktív")
    
    st.write("---")
    st.subheader("🔔 Időzített Értesítések (30, 15, 7 nap)")
    
    found_notification = False
    
    for emp in st.session_state.employees:
        d_sz = get_diff(emp['Szerződés vége'])
        d_orv = get_diff(emp['Orvosi lejárat'])
        d_tud = get_diff(emp['Tüdőszűrő lejárat'])
        
        milestones = [30, 15, 7]
        
        # 1. ADMIN ÉRTESÍTÉSEK (Szerződés vége)
        if d_sz in milestones or d_sz < 0:
            found_notification = True
            st.error(f"📩 **ADMIN ÉRTESÍTÉS** ({st.session_state.admin_email_1}, {st.session_state.admin_email_2})\n\n "
                     f"ALKALMAZOTT: {emp['Név']} | ESEMÉNY: Munkaszerződés lejár {d_sz} nap múlva!")

        # 2. DOLGOZÓI ÉRTESÍTÉSEK (Orvosi és Tüdőszűrő)
        emp_issues = []
        if d_orv in milestones or d_orv < 0:
            emp_issues.append(f"⚕️ Orvosi alkalmasság ({d_orv} nap)")
        if d_tud in milestones or d_tud < 0:
            emp_issues.append(f"🫁 Tüdőszűrő ({d_tud} nap)")
            
        if emp_issues:
            found_notification = True
            st.warning(f"📩 **DOLGOZÓI ÉRTESÍTÉS** ({emp['Email']})\n\n "
                       f"ALKALMAZOTT: {emp['Név']} | TEENDŐ: " + " & ".join(emp_issues))
    
    if not found_notification:
        st.success("Nincs mára ütemezett értesítés.")

# --- ALKALMAZOTTAK NÉZET ---
elif menu == "Alkalmazottak":
    st.header("👥 Alkalmazottak kezelése")
    
    with st.expander("➕ Új alkalmazott rögzítése"):
        with st.form("add_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            nev = c1.text_input("Név")
            email = c2.text_input("Dolgozó Email címe")
            
            c_sz, c_o, c_t = st.columns(3)
            sz_v = c_sz.date_input("Szerződés vége")
            orv = c_o.date_input("Orvosi lejárat")
            tud = c_t.date_input("Tüdőszűrő lejárat")
            
            if st.form_submit_button("Mentés"):
                if nev and email:
                    st.session_state.employees.append({
                        "Név": nev, "Email": email, 
                        "Szerződés vége": str(sz_v), 
                        "Orvosi lejárat": str(orv), 
                        "Tüdőszűrő lejárat": str(tud)
                    })
                    st.rerun()
                else:
                    st.error("Név és Email kötelező!")

    st.write("---")
    if st.session_state.employees:
        for i, emp in enumerate(st.session_state.employees):
            cols = st.columns([2, 2, 2, 2, 1])
            cols[0].write(f"**{emp['Név']}**")
            cols[1].write(emp['Email'])
            cols[2].write(f"Szerz: {emp['Szerződés vége']}")
            cols[3].write(f"Orv: {emp['Orvosi lejárat']}")
            if cols[4].button("🗑️", key=f"del_btn_{i}"):
                st.session_state.employees.pop(i)
                st.rerun()
    else:
        st.info("Nincsenek rögzített adatok.")

# --- BEÁLLÍTÁSOK ---
elif menu == "Beállítások":
    st.header("⚙️ Rendszerbeállítások")
    
    st.subheader("Adminisztrátori értesítések (Szerződés lejárat)")
    st.session_state.admin_email_1 = st.text_input("Admin 1 Email", value=st.session_state.admin_email_1)
    st.session_state.admin_email_2 = st.text_input("Admin 2 Email", value=st.session_state.admin_email_2)
    
    st.subheader("Email küldő (SMTP) adatok")
    st.text_input("SMTP Szerver")
    st.text_input("Port (pl. 587)")
    st.text_input("Jelszó", type="password")
    
    if st.button("Beállítások mentése"):
        st.success("Beállítások rögzítve!")
