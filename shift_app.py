import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
import streamlit_authenticator as stauth
import os

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
    workers_df = pd.read_csv("workers.csv")
    positions_df = pd.read_csv("positions.csv")
    workers = workers_df['name'].tolist()
    workers_gender = dict(zip(workers_df['name'], workers_df['gender']))

    # הגדרת עמדות סיור לזכרים בלבד
    patrol_positions = ["סיור 10", "סיור 10א"]

    # טען או צור טבלת שיבוצים
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

    for pos in positions_df['position']:
        st.markdown(f"### עמדה: {pos}")
        cols = st.columns(len(DAYS))

        for d_idx, day in enumerate(DAYS):
            with cols[d_idx]:
                for shift in SHIFT_TIMES:
                    key = f"{pos}__{day}__{shift}"
                    current = schedule.loc[key, 'name'] if key in schedule.index else ""

                    label = f"{day} {shift}"
                    if role == 'admin':
                        # סינון לפי מין בעמדות סיור
                        if pos in patrol_positions:
                            male_workers = [w for w in workers if workers_gender.get(w) == 'זכר']
                            selection = st.selectbox(label, [""] + male_workers, key=key, index=[""] + male_workers.index(current) if current in male_workers else 0)
                        else:
                            selection = st.selectbox(label, [""] + workers, key=key, 
                                                     if current in workers:
                                                        index_val = workers.index(current) + 1  # +1 בגלל שהוספנו "" בתחילת הרשימה
                                                    else:
                                                        index_val = 0
                                                        selection = st.selectbox(label, [\"\"] + workers, key=key, index=index_val))
                        edited_schedule.loc[key, 'name'] = selection
                    else:
                        st.markdown(f"**{label}:** {current if current else '-'}")

    if role == 'admin' and st.button("💾 שמור שיבוצים"):
        edited_schedule.to_csv(SCHEDULE_FILE)
        st.success("השיבוצים נשמרו בהצלחה!")


