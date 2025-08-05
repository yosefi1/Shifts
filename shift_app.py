import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
import streamlit_authenticator as stauth
import os
import hashlib
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

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
    workers_df = pd.read_csv("workers.csv", encoding='utf-8-sig')
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

    # --- עיצוב RTL ויישור ---
    st.markdown("""
        <style>
        div[data-testid="stMarkdownContainer"] {
            direction: rtl;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📅 טבלת שיבוצים שבועית")

    role = config['credentials']['usernames'][username]['role']
    edited_schedule = schedule.copy()

    # --- בניית DataFrame לטבלה ---
    table_data = []
    for pos in positions_df['position']:
        row = {"עמדה": pos}
        for day in DAYS:
            for shift in SHIFT_TIMES:
                key = f"{day} {shift}"
                index_key = f"{pos}__{day}__{shift}"
                row[key] = schedule.loc[index_key, 'name'] if index_key in schedule.index else ""
        table_data.append(row)

    df = pd.DataFrame(table_data)

    # --- הגדרות AGGRID ---
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=(role == 'admin'), resizable=True, wrapText=True, autoHeight=True)
    gb.configure_grid_options(domLayout='normal', suppressRowClickSelection=False)
    gb.configure_columns(df.columns[1:], cellEditor='agSelectCellEditor', cellEditorParams={"values": workers})
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=False,
        height=600,
        reload_data=False
    )

    updated_df = grid_response['data']

    if role == 'admin' and st.button("💾 שמור שיבוצים"):
        for idx, row in updated_df.iterrows():
            pos = row['עמדה']
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    col = f"{day} {shift}"
                    index_key = f"{pos}__{day}__{shift}"
                    edited_schedule.loc[index_key, 'name'] = row[col]
        edited_schedule.to_csv(SCHEDULE_FILE)
        st.success("השיבוצים נשמרו בהצלחה!")
