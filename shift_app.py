import streamlit as st
from aggrid_component import aggrid_component

st.title("📅 מערכת שיבוצים")
st.subheader("🔧 Test AG Grid Component")

data = [
    {"position": "א'", "ראשון 08:00-12:00": "", "ראשון 12:00-20:00": ""},
    {"position": "ב'", "ראשון 08:00-12:00": "יוסי", "ראשון 12:00-20:00": ""},
]
columns = ["ראשון 08:00-12:00", "ראשון 12:00-20:00"]
workers = ["⬇ בחר", "יוסי", "דוד", "שרה"]

try:
    result = aggrid_component(data=data, workers=workers, columns=columns)
    if result:
        st.success("✅ Updated table received!")
        st.write(result)
except Exception as e:
    st.error(f"Component error: {e}")
