import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

from views.view_schedule import show_schedule_tab
from views.mark_constraints import show_constraints_tab
from utils.helpers import SHIFT_TIMES, DAYS
from views.view_constraints_admin import show_admin_constraints_view

# --- Load config ---
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

    # Page styling (RTL)
    st.markdown("""
        <style>
        div[data-testid="stMarkdownContainer"] {
            direction: rtl;
            text-align: right;
        }
        .block-container {
            padding: 0 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Tabs
    tabs = ["📅 צפייה בשיבוצים"]
    if role != "admin":
        tabs.append("🚫 סימון אילוצים")
    if role == "admin":
        tabs.append("👀 צפייה באילוצי עובדים")
    
    selected_tab = st.selectbox("בחר תצוגה", tabs)
    
    if selected_tab == "📅 שיבוץ":
        show_schedule_tab(role)
    elif selected_tab == "🚫 סימון אילוצים":
        show_constraints_tab(username)
    elif selected_tab == "👀 אילוצים":
        show_admin_constraints_view()




