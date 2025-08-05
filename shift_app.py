import streamlit as st
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os
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
        .block-container {
            padding: 0 1rem;
        }
        .ag-theme-streamlit .ag-header-cell-label {
            white-space: normal !important;
            text-align: center;
            font-weight: bold;
        }
        .ag-theme-streamlit .ag-header {
            font-weight: bold;
            background-color: #f5f5f5;
        }
        .ag-theme-streamlit .ag-cell {
            line-height: 1.6 !important;
            border-right: 1px solid #ddd !important;
            text-align: center;
        }
        .ag-theme-streamlit .ag-row {
            border-bottom: 1px solid #ddd !important;
        }
        .ag-root-wrapper {
            width: 100% !important;
        }
        .ag-select-cell-editor {
            width: 100% !important;
        }
        .ag-cell-focus {
            border: 1px solid #007bff !important;
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
    gb.configure_default_column(
        editable=(role == 'admin'),
        resizable=True,
        wrapText=True,
        autoHeight=True,
        singleClickEdit=True,
        cellStyle={"textAlign": "center"}
    )
    gb.configure_grid_options(
        domLayout='normal',
        suppressRowClickSelection=False,
        stopEditingWhenCellsLoseFocus=True
    )

    for col in df.columns:
        if col == 'עמדה':
            gb.configure_column(
                col,
                width=150,
                wrapText=True,
                autoHeight=True,
                pinned='left'
            )
        else:
            gb.configure_column(
                col,
                cellEditor='agSelectCellEditor',
                cellEditorParams={"values": [""] + workers},
                cellRenderer='agGroupCellRenderer',
                width=120,
                wrapText=True,
                autoHeight=True
            )

    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=False,
        enable_enterprise_modules=False,
        allow_unsafe_jscode=True,
        reload_data=False,
        height=600,
        theme="streamlit",
        custom_css={
            ".ag-cell": {
                "border-right": "1px solid #ccc !important",
                "border-bottom": "1px solid #ccc !important",
                "text-align": "center",
            },
            ".ag-header-cell": {
                "border-right": "1px solid #ccc !important",
                "background-color": "#f5f5f5",
                "font-weight": "bold",
            },
            ".ag-select-cell-editor": {
                "width": "100% !important",
            },
            ".ag-cell-focus": {
                "border": "1px solid #007bff !important",
            }
        }
    )

    updated_df = grid_response['data']

    if role == 'admin' and st.button("📅 שמור שיבוצים"):
        for idx, row in updated_df.iterrows():
            pos = row['עמדה']
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    col = f"{day} {shift}"
                    index_key = f"{pos}__{day}__{shift}"
                    edited_schedule.loc[index_key, 'name'] = row[col]
        edited_schedule.to_csv(SCHEDULE_FILE)
        st.success("השיבוצים נשמרו בהצלחה!")
