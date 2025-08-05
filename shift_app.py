import streamlit as st
import pandas as pd

# Sample data like your shift table
SHIFT_TIMES = ["08:00-12:00", "12:00-20:00", "20:00-00:00"]
DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
positions = ["א'", "ב'", "ג'"]
workers = ["⬇ בחר", "דוד", "יוסי", "שרה"]

# Build sample DataFrame
data = []
for pos in positions:
    row = {"עמדה": pos}
    for day in DAYS:
        for shift in SHIFT_TIMES:
            col_name = f"{day} {shift}"
            row[col_name] = ""
    data.append(row)

df = pd.DataFrame(data)

# Editable config with dropdowns
edit_config = {}
for col in df.columns:
    if col != "עמדה":
        edit_config[col] = st.column_config.SelectboxColumn(
            label=col,
            options=workers,
            required=False
        )

# Show editable table
edited_df = st.data_editor(
    df,
    column_config=edit_config,
    use_container_width=True,
    num_rows="dynamic",
    hide_index=True
)

# Save button
if st.button("📅 שמור שיבוצים"):
    st.success("השיבוצים נשמרו בהצלחה!")
    # Save edited_df to CSV or DB
