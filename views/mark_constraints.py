import streamlit as st
import pandas as pd
import os
from utils.helpers import DAYS

CONSTRAINT_DIR = "constraints"

# שעות משמרת מותאמות לכל יום
CUSTOM_SHIFT_TIMES_PER_DAY = {
    "ראשון": ["20:00-00:00"],
    "שני": ["08:00-12:00", "12:00-20:00"],
    "שלישי": ["08:00-12:00", "12:00-20:00"],
    "רביעי": ["08:00-12:00", "12:00-20:00"],
    "חמישי": ["08:00-12:00", "12:00-20:00"],
    "שישי": ["08:00-12:00", "12:00-20:00"],
    "שבת": ["08:00-12:00", "12:00-20:00"],
    "ראשון שאחריו": ["08:00-12:00"]
}

def show_constraints_tab(username):
    st.subheader("🚫 סימון אילוצים לשבוע הבא")

    os.makedirs(CONSTRAINT_DIR, exist_ok=True)
    constraint_file = os.path.join(CONSTRAINT_DIR, f"{username}_constraints.csv")
    note_file = os.path.join(CONSTRAINT_DIR, f"{username}_note.txt")

    # יצירת טבלה
    data = []
    for day, shifts in CUSTOM_SHIFT_TIMES_PER_DAY.items():
        row = {"יום": day}
        for shift in shifts:
            row[shift] = False
        data.append(row)

    df = pd.DataFrame(data)

    # טעינת אילוצים קיימים
    if os.path.exists(constraint_file):
        try:
            df_marked = pd.read_csv(constraint_file)
            for _, row in df_marked.iterrows():
                day, shift = row["day"], row["shift"]
                if day in df["יום"].values and shift in df.columns:
                    df.loc[df["יום"] == day, shift] = True
        except Exception as e:
            st.error(f"שגיאה בטעינת אילוצים קודמים: {e}")

    # טבלת סימון עם AgGrid
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
    gb.configure_grid_options(domLayout='normal')

    for col in df.columns:
        if col == "יום":
            gb.configure_column(col, editable=False, pinned='left', width=150)
        else:
            gb.configure_column(col, editable=True, cellEditor='agCheckboxCellEditor', width=140)

    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        theme="streamlit",
        height=500,
        allow_unsafe_jscode=True,
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
            ".ag-cell-focus": {
                "border": "1px solid #007bff !important",
            }
        }
    )

    updated_df = grid_response['data']

    # הערה
    st.markdown("### הערה למנהל (לא חובה):")
    note = ""
    if os.path.exists(note_file):
        with open(note_file, "r", encoding='utf-8') as f:
            note = f.read()
    note_input = st.text_area("הקלד הערה", value=note)

    # כפתור שמירה
    if st.button("💾 שמור אילוצים"):
        blocked = []
        for idx, row in updated_df.iterrows():
            day = row["יום"]
            for shift in CUSTOM_SHIFT_TIMES_PER_DAY.get(day, []):
                if row.get(shift) == True:
                    blocked.append((day, shift))

        df_save = pd.DataFrame(blocked, columns=["day", "shift"])
        df_save.to_csv(constraint_file, index=False, encoding='utf-8-sig')

        with open(note_file, "w", encoding='utf-8') as f:
            f.write(note_input)

        st.success("האילוצים נשמרו בהצלחה!")
