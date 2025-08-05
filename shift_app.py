import streamlit as st
from dropdown_component import dropdown_component
import json

# Sample data
data = [
    {"עמדה": "A", "ראשון 08:00-12:00": "", "ראשון 12:00-20:00": "", "ראשון 20:00-00:00": ""},
    {"עמדה": "B", "ראשון 08:00-12:00": "", "ראשון 12:00-20:00": "", "ראשון 20:00-00:00": ""}
]

columns = ["ראשון 08:00-12:00", "ראשון 12:00-20:00", "ראשון 20:00-00:00"]
workers = ["יוסי", "טל", "דני"]

st.title("📋 טבלת שיבוצים - Dropdown Demo")

# Serialize to JSON
data_json = json.dumps(data)
columns_json = json.dumps(columns)
workers_json = json.dumps(workers)

# Call component
result = dropdown_component(data=data_json, columns=columns_json, workers=workers_json)

st.write("Result:")
st.write(result)
