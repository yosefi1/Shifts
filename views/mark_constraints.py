import streamlit as st
import os
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

CONSTRAINT_DIR = "constraints"


def show_admin_constraints_view():
    st.subheader("📋 צפייה באילוצים של עובדים")

    if not os.path.exists(CONSTRAINT_DIR):
        st.info("אין אילוצים להצגה עדיין.")
        return

    usernames = [f.split("_constraints.csv")[0] for f in os.listdir(CONSTRAINT_DIR) if f.endswith("_constraints.csv")]
    if not usernames:
        st.info("אין אילוצים להצגה עדיין.")
        return

    selected_user = st.selectbox("בחר עובד לצפייה באילוצים:", usernames)

    constraint_file = os.path.join(CONSTRAINT_DIR, f"{selected_user}_constraints.csv")
    note_file = os.path.join(CONSTRAINT_DIR, f"{selected_user}_note.txt")

    st.markdown(f"### אילוצים של {selected_user}")

    try:
        df = pd.read_csv(constraint_file)
    except Exception as e:
        st.error(f"שגיאה בטעינת הקובץ: {e}")
        return

    if df.empty:
        st.info("אין אילוצים רשומים לעובד זה.")
    else:
        pivot = df.pivot(index="position", columns=["day", "shift"], values="blocked")
        pivot.fillna("", inplace=True)

        gb = GridOptionsBuilder.from_dataframe(pivot)
        gb.configure_default_column(resizable=True, wrapText=True, autoHeight=True)
        gb.configure_grid_options(domLayout='normal')
        grid_options = gb.build()

        AgGrid(
            pivot,
            gridOptions=grid_options,
            height=500,
            fit_columns_on_grid_load=True,
            theme="streamlit"
        )

    if os.path.exists(note_file):
        with open(note_file, "r", encoding='utf-8') as f:
            note = f.read().strip()
        if note:
            st.markdown("### הערת העובד:")
            st.info(note)
        else:
            st.markdown("(ללא הערה)")
    else:
        st.markdown("(ללא קובץ הערה)")
