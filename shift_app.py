import streamlit as st
import pandas as pd

# Create a fake table layout
positions = ['א׳', 'ב׳']
DAYS = ["ראשון", "שני"]
SHIFTS = ["08:00-12:00", "12:00-20:00"]
workers = ["⬇ בחר", "דוד", "יוסי", "שרה"]

st.markdown("## טבלת שיבוצים")

for pos in positions:
    st.markdown(f"### {pos}")
    for day in DAYS:
        for shift in SHIFTS:
            key = f"{pos}__{day}__{shift}"
            st.selectbox(
                f"{day} {shift}",
                workers,
                key=key
            )
