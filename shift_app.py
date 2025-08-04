import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime

# Load config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status is False:
    st.error("שם משתמש או סיסמה לא נכונים")

if authentication_status is None:
    st.warning("אנא התחבר")

if authentication_status:
    st.sidebar.success(f"שלום {name}")
    authenticator.logout("התנתקות", "sidebar")

    ROLE = config['credentials']['usernames'][username]['role']
    FILENAME = "constraints.csv"
    SHIFTS = ["בוקר", "צהריים", "ערב"]
    DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    st.title("🗓️ מערכת הזנת אילוצים לשיבוץ משמרות")

    # עובד רגיל: הזנת אילוצים
    if ROLE == "user":
        st.header("הזנת אילוצים לשבוע הקרוב")
        unavailable = []

        st.markdown("בחר אילוצים (שבהם אינך יכול לעבוד):")
        for day in DAYS:
            cols = st.columns(len(SHIFTS))
            for i, shift in enumerate(SHIFTS):
                key = f"{day}_{shift}"
                if cols[i].checkbox(f"{day} - {shift}", key=key):
                    unavailable.append((day, shift))

        comment = st.text_area("הערות נוספות")

        if st.button("שמור אילוצים"):
            entry = {
                "משתמש": username,
                "שם": name,
                "תאריך שליחה": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "אילוצים": "; ".join([f"{d} ({s})" for d, s in unavailable]),
                "הערות": comment
            }

            try:
                df = pd.read_csv(FILENAME)
            except FileNotFoundError:
                df = pd.DataFrame(columns=entry.keys())

            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
            df.to_csv(FILENAME, index=False)
            st.success("✅ האילוצים נשמרו בהצלחה!")

    # מנהל: צפייה באילוצים של כולם
    if ROLE == "admin":
        st.header("👀 צפייה באילוצים של כלל העובדים")

        try:
            df = pd.read_csv(FILENAME)
            st.dataframe(df)
        except FileNotFoundError:
            st.info("אין עדיין אילוצים במערכת.")

        st.markdown("---")
        st.subheader("📆 תצוגת לוח שבועי")

        # טבלת אילוצים לפי ימים ומשמרות
        table = pd.DataFrame(index=SHIFTS, columns=DAYS)

        # בונה מילון של אילוצים
        try:
            constraints_df = pd.read_csv(FILENAME)
            all_constraints = {}
            for _, row in constraints_df.iterrows():
                name = row["שם"]
                items = row["אילוצים"].split("; ")
                for item in items:
                    if " (" in item:
                        d, s = item.replace(")", "").split(" (")
                        all_constraints.setdefault((d, s), []).append(name)
        except:
            all_constraints = {}

        for day in DAYS:
            for shift in SHIFTS:
                key = (day, shift)
                names = all_constraints.get(key, [])
                table.at[shift, day] = ", ".join(names)

        st.dataframe(table.fillna("—"))


