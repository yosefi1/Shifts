# views/mark_constraints.py

import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.helpers import SHIFT_TIMES, DAYS

def show_constraints_tab(username):
    st.subheader("🚫 אילוצים לשבוע הבא")
    st.info("סמן אילוצים - באילו משמרות אינך יכול לעבוד")

    positions_df = pd.read_csv("positions.csv", encoding="utf-8")
    constraint_file = f"data/constraints__{username}.csv"

    # Build empty table if not exists
    if os.path.exists(constraint_file):
        df = pd.read_csv(constraint_file)
    else:
        table_data = []
        for pos in positions_df['position']:
            row = {"עמדה": pos}
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    key = f"{day} {shift}"
                    row[key] = "יכול"
            table_data.append(row)
        df = pd.DataFrame(table_data)

    # AG Grid config
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        editable=True,
        resizable=True,
        wrapText=True,
        autoHeight=True,
        singleClickEdit=True,
        cellEditor='agSelectCellEditor',
        cellEditorParams={'values': ["יכול", "לא יכול"]},
        cellStyle={"textAlign": "center"}
    )
    gb.configure_column("עמדה", editable=False, pinned='left', width=150)

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

    if st.button("💾 שמור אילוצים"):
        updated_df = grid_response['data']
        os.makedirs("data", exist_ok=True)
        updated_df.to_csv(constraint_file, index=False)
        st.success("האילוצים נשמרו בהצלחה!")
