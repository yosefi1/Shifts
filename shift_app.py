from aggrid_component import aggrid_component

# Example usage
data = [{"position": "א'", "ראשון 08:00-12:00": ""}]
columns = ["ראשון 08:00-12:00"]
workers = ["⬇ בחר", "יוסי", "דוד"]

result = aggrid_component(data=data, workers=workers, columns=columns)
if result:
    st.write(result)
