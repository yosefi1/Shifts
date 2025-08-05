import streamlit as st
from dropdown_component import dropdown_component


st.title("📋 טבלת שיבוצים - Dropdown Demo")

data = [
    {"position": "א'", "ראשון 08:00-12:00": "", "ראשון 12:00-20:00": ""},
    {"position": "ב'", "ראשון 08:00-12:00": "יוסי", "ראשון 12:00-20:00": ""},
]
columns = ["ראשון 08:00-12:00", "ראשון 12:00-20:00"]
workers = ["⬇ בחר", "יוסי", "דוד", "שרה"]

result = dropdown_component(data=data, columns=columns, workers=workers)
if result:
    st.success("✅ טבלה עודכנה")
    st.write(result)


