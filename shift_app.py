import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
import streamlit_authenticator as stauth
import os
import hashlib

# --- הגדרות ---
SHIFT_TIMES = ["08:00-12:00", "12:00-20:00", "20:00-00:00"]
DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
SCHEDULE_FILE = "schedule.csv"

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

    # טען עובדים ועמדות
    workers_df = pd.read_csv("workers.csv", encoding='utf-8')
    positions_df = pd.read_csv("positions.csv", encoding='utf-8')
    workers = workers_df['name'].tolist()
    workers_gender = dict(zip(workers_df['name'], workers_df['gender']))

    patrol_positions = ["סיור 10", "סיור 10א"]

    if os.path.exists(SCHEDULE_FILE):
        schedule = pd.read_csv(SCHEDULE_FILE, index_col=0)
    else:
        index = []
        for pos in positions_df['position']:
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    index.append(f"{pos}__{day}__{shift}")
        schedule = pd.DataFrame(index=index, columns=['name'])

    st.title("📅 טבלת שיבוצים שבועית")

    role = config['credentials']['usernames'][username]['role']
    edited_schedule = schedule.copy()
    used_keys = set()

    # שורת כותרות
    header_cols = st.columns(len(SHIFT_TIMES) * len(DAYS) + 1)
    header_cols[0].markdown("**עמדה**")
    for i, day in enumerate(DAYS):
        for shift in SHIFT_TIMES:
            idx = 1 + i * len(SHIFT_TIMES) + SHIFT_TIMES.index(shift)
            header_cols[idx].markdown(f"**{day}<br>{shift}**", unsafe_allow_html=True)

    # שורות של עמדות
    for pos in positions_df['position']:
        row_cols = st.columns(len(SHIFT_TIMES) * len(DAYS) + 1)
        row_cols[0].markdown(f"**{pos}**")

        col_idx = 1
        for day in DAYS:
            for shift in SHIFT_TIMES:
                full_index = f"{pos}__{day}__{shift}"
                current = schedule.loc[full_index, 'name'] if full_index in schedule.index else ""
                current_str = str(current).strip()

                key_base = f"{pos}_{day}_{shift}"
                key = hashlib.md5(key_base.encode()).hexdigest()[:10]
                while key in used_keys:
                    key_base += "_"
                    key = hashlib.md5(key_base.encode()).hexdigest()[:10]
                used_keys.add(key)

                with row_cols[col_idx]:
                    if role == 'admin':
                        if pos in patrol_positions:
                            male_workers = [w for w in workers if workers_gender.get(w) == 'זכר']
                            index_val = male_workers.index(current_str) + 1 if current_str in male_workers else 0
                            cell = st.selectbox("", [""] + male_workers, key=key, index=index_val, label_visibility="collapsed")
                        else:
                            index_val = workers.index(current_str) + 1 if current_str in workers else 0
                            cell = st.selectbox("", [""] + workers, key=key, index=index_val, label_visibility="collapsed")
                        edited_schedule.loc[full_index, 'name'] = cell
                    else:
                        st.markdown(f"{current_str if current_str else '-'}")

                col_idx += 1

    if role == 'admin' and st.button("💾 שמור שיבוצים"):
        edited_schedule.to_csv(SCHEDULE_FILE)
        st.success("השיבוצים נשמרו בהצלחה!")
