import streamlit as st
from dropdown_component import dropdown_component

# Sample data
data = [
    {"עמדה": "A", "ראשון 08:00-12:00": "", "ראשון 12:00-20:00": "", "ראשון 20:00-00:00": ""},
    {"עמדה": "B", "ראשון 08:00-12:00": "", "ראשון 12:00-20:00": "", "ראשון 20:00-00:00": ""}
]

columns = ["ראשון 08:00-12:00", "ראשון 12:00-20:00", "ראשון 20:00-00:00"]
workers = ["יוסי", "טל", "דני"]

st.title("📋 טבלת שיבוצים - Dropdown Demo")

result = dropdown_component(data=data, columns=columns, workers=workers)

st.write("Result:")
st.write(result)
