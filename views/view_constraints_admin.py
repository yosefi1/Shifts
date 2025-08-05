import streamlit as st
import os
import pandas as pd

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
    df = pd.read_csv(constraint_file)
    st.dataframe(df)

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
