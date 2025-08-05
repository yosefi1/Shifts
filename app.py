# app.py

import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

from views.view_schedule import show_schedule_tab
from views.mark_constraints import show_constraints_tab

# --- הגדרות ---
st.set_page_config(page_title="מערכת שיבוצים", layout="wide")

# --- טעינת קונפיג ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, auth_status, username = authenticator.login("Login", "main")

if auth_status is False:
    st.error("שם משתמש או סיסמה לא נכונים")
elif auth_status is None:
    st.warning("אנא התחבר")
else:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"שלום {name}")

    role = config['credentials']['usernames'][username]['role']

    tab1, tab2 = st.tabs(["📅 צפייה בשיבוצים", "🚫 סימון אילוצים"])

    with tab1:
        show_schedule_tab(role)

    with tab2:
        show_constraints_tab(username)
