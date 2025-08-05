# views/view_schedule.py

import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.helpers import load_schedule, build_schedule_table, SHIFT_TIMES, DAYS

def show_schedule_tab(role):
    st.subheader("📅 טבלת שיבוצים שבועית")

    # Load data
    schedule = load_schedule()
    positions_df = pd.read_csv("positions.csv", encoding="utf-8")

    df = build_schedule_table(schedule, positions_df)

    # AG Grid setup
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=(role == 'admin'),
        resizable=True,
        wrapText=True,
        autoHeight=True,
        singleClickEdit=True,
        cellStyle={"textAlign": "center"}
    )
    for col in df.columns:
        if col == 'עמדה':
            gb.configure_column(col, pinned='left', width=150)
        else:
            gb.configure_column(col, width=140)

    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode="VALUE_CHANGED",
        height=600,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        theme="streamlit"
    )

    # Save only if admin
    if role == 'admin' and st.button("📥 שמור שיבוצים"):
        updated_df = grid_response['data']
        new_schedule = pd.DataFrame(index=schedule.index, columns=['name'])
        for idx, row in updated_df.iterrows():
            pos = row['עמדה']
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    col = f"{day} {shift}"
                    index_key = f"{pos}__{day}__{shift}"
                    new_schedule.loc[index_key, 'name'] = row[col]
        new_schedule.to_csv("schedule.csv")
        st.success("השיבוצים נשמרו בהצלחה!")
