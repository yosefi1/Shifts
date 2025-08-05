import streamlit as st
import pandas as pd
import os
from utils.helpers import DAYS

CONSTRAINT_DIR = "constraints"

# שעות משמרת מותאמות לכל יום
SHIFT_STRUCTURE = {
    "ראשון": ["20:00-00:00"],
    "שני": ["08:00-12:00", "12:00-20:00"],
    "שלישי": ["08:00-12:00", "12:00-20:00"],
    "רביעי": ["08:00-12:00", "12:00-20:00"],
    "חמישי": ["08:00-12:00", "12:00-20:00"],
    "שישי": ["08:00-12:00", "12:00-20:00"],
    "שבת": ["08:00-12:00", "12:00-20:00"],
    "ראשון שאחריו": ["08:00-12:00"]
}

def show_constraints_tab(username):
    st.subheader("🚫 סימון אילוצים לשבוע הבא")

    os.makedirs(CONSTRAINT_DIR, exist_ok=True)
    constraint_file = os.path.join(CONSTRAINT_DIR, f"{username}_constraints.csv")
    note_file = os.path.join(CONSTRAINT_DIR, f"{username}_note.txt")

    # יצירת טבלה עם כל המשמרות
    all_shifts = ["08:00-12:00", "12:00-20:00"]
    table_data = []
    for day, shifts in SHIFT_STRUCTURE.items():
        row = {"יום": day}
        for shift in all_shifts:
            row[shift] = False if shift in shifts else None
        table_data.append(row)
    df = pd.DataFrame(table_data).set_index("יום")

    # טעינת אילוצים קיימים
    if os.path.exists(constraint_file):
        try:
            df_marked = pd.read_csv(constraint_file)
            for _, row in df_marked.iterrows():
                day, shift = row["day"], row["shift"]
                if day in df.index and shift in df.columns:
                    df.at[day, shift] = True
        except Exception as e:
            st.error(f"שגיאה בטעינת אילוצים קודמים: {e}")

    # טבלת סימון עם צ'קבוקסים
    st.markdown("### סמן את המשמרות בהן אינך יכול לעבוד:")
    updated_rows = []
    for day in df.index:
        cols = st.columns(len(all_shifts) + 1)
        cols[0].markdown(f"**{day}**")
        row = {"יום": day}
        for i, shift in enumerate(all_shifts):
            if SHIFT_STRUCTURE.get(day) and shift in SHIFT_STRUCTURE[day]:
                key = f"{day}_{shift}_{username}"
                row[shift] = cols[i + 1].checkbox("", value=bool(df.at[day, shift]), key=key)
            else:
                cols[i + 1].markdown("❌")
                row[shift] = None
        updated_rows.append(row)

    updated_df = pd.DataFrame(updated_rows).set_index("יום")

    # הערה
    st.markdown("### הערה למנהל (לא חובה):")
    note = ""
    if os.path.exists(note_file):
        with open(note_file, "r", encoding='utf-8') as f:
            note = f.read()
    note_input = st.text_area("הקלד הערה", value=note)

    # כפתור שמירה
    if st.button("💾 שמור אילוצים"):
        blocked = []
        for day in updated_df.index:
            for shift in all_shifts:
                if updated_df.at[day, shift] == True:
                    blocked.append((day, shift))

        df_save = pd.DataFrame(blocked, columns=["day", "shift"])
        df_save.to_csv(constraint_file, index=False, encoding='utf-8-sig')

        with open(note_file, "w", encoding='utf-8') as f:
            f.write(note_input)

        st.success("האילוצים נשמרו בהצלחה!")
