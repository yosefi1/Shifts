# views/view_schedule.py

import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from utils.helpers import SHIFT_TIMES, DAYS, load_schedule, build_schedule_table

def show_schedule_tab(role):
    st.subheader("📅 טבלת שיבוצים שבועית")

    workers_df = pd.read_csv("workers.csv", encoding='utf-8-sig')
    positions_df = pd.read_csv("positions.csv", encoding='utf-8')
    workers = workers_df['name'].tolist()

    schedule = load_schedule()
    edited_schedule = schedule.copy()
    df = build_schedule_table(schedule, positions_df)

    # --- AG Grid setup (like your original code) ---
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
        stopEditingWhenCellsLoseFocus=True,
        rowSelection='single'
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
                cellEditorParams={"values": ["⬇ בחר"] + workers},
                width=140,
                wrapText=True,
                autoHeight=True,
                editable=(role == 'admin'),
                singleClickEdit=True
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
        edited_schedule.to_csv("schedule.csv")
        st.success("השיבוצים נשמרו בהצלחה!")
