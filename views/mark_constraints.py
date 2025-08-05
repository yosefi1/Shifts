import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from utils.helpers import SHIFT_TIMES, DAYS

CONSTRAINT_DIR = "constraints"

def show_constraints_tab(username):
    st.subheader("🚫 סימון אילוצים לשבוע הבא")

    # Load positions
    positions_df = pd.read_csv("positions.csv", encoding='utf-8')
    positions = positions_df['position'].tolist()

    # Load existing constraints if available
    os.makedirs(CONSTRAINT_DIR, exist_ok=True)
    constraint_file = os.path.join(CONSTRAINT_DIR, f"{username}_constraints.csv")
    note_file = os.path.join(CONSTRAINT_DIR, f"{username}_note.txt")

    if os.path.exists(constraint_file):
        constraints_df = pd.read_csv(constraint_file)
        marked = {(row['position'], row['day'], row['shift']) for _, row in constraints_df.iterrows()}
    else:
        marked = set()

    # Create empty grid DataFrame
    table_data = []
    for pos in positions:
        row = {"עמדה": pos}
        for day in DAYS:
            for shift in SHIFT_TIMES:
                key = f"{day} {shift}"
                row[key] = "❌" if (pos, day, shift) in marked else ""
        table_data.append(row)

    df = pd.DataFrame(table_data)

    # Grid config
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, wrapText=True, autoHeight=True)
    for col in df.columns:
        gb.configure_column(col, width=110)
    gb.configure_column("עמדה", pinned='left', editable=False, width=150)
    gb.configure_grid_options(stopEditingWhenCellsLoseFocus=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=True,
        height=600,
        theme="streamlit"
    )

    updated_df = grid_response["data"]

    # Note box
    st.markdown("### הערה למנהל (לא חובה):")
    note = ""
    if os.path.exists(note_file):
        with open(note_file, "r", encoding='utf-8') as f:
            note = f.read()
    note_input = st.text_area("הקלד הערה", value=note)

    # Save
    if st.button("💾 שמור אילוצים"):
        new_constraints = []
        for idx, row in updated_df.iterrows():
            pos = row["עמדה"]
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    key = f"{day} {shift}"
                    if row.get(key) == "❌":
                        new_constraints.append((pos, day, shift))

        df_to_save = pd.DataFrame(new_constraints, columns=["position", "day", "shift"])
        df_to_save["blocked"] = "❌"
        df_to_save.to_csv(constraint_file, index=False, encoding='utf-8-sig')

        with open(note_file, "w", encoding='utf-8') as f:
            f.write(note_input)

        st.success("האילוצים נשמרו בהצלחה!")
