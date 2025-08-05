import streamlit as st
import pandas as pd
import os
from utils.helpers import DAYS

CONSTRAINT_DIR = "constraints"

# שעות משמרת מותאמות לכל יום
CUSTOM_SHIFT_TIMES_PER_DAY = {
    "ראשון": ["20:00-00:00"],
    "שני": ["08:00-12:00", "12:00-20:00"],
    "שלישי": ["08:00-12:00", "12:00-20:00"],
    "רביעי": ["08:00-12:00", "12:00-20:00"],
    "חמישי": ["08:00-12:00", "12:00-20:00"],
    "שישי": ["08:00-12:00", "12:00-20:00"],
    "שבת": ["08:00-12:00", "12:00-20:00"],
    "ראשון שאחרי": ["08:00-12:00"]
}

def show_constraints_tab(username):
    st.subheader("🚫 סימון אילוצים לשבוע הבא")

    os.makedirs(CONSTRAINT_DIR, exist_ok=True)
    constraint_file = os.path.join(CONSTRAINT_DIR, f"{username}_constraints.csv")
    note_file = os.path.join(CONSTRAINT_DIR, f"{username}_note.txt")

    # יצירת טבלה
    data = []
    for day, shifts in CUSTOM_SHIFT_TIMES_PER_DAY.items():
        row = {"יום": day}
        for shift in shifts:
            row[shift] = False
        data.append(row)

    df = pd.DataFrame(data)

    # טעינת אילוצים קיימים
    if os.path.exists(constraint_file):
        try:
            df_marked = pd.read_csv(constraint_file)
            for _, row in df_marked.iterrows():
                day, shift = row["day"], row["shift"]
                if day in df["יום"].values and shift in df.columns:
                    df.loc[df["יום"] == day, shift] = True
        except Exception as e:
            st.error(f"שגיאה בטעינת אילוצים קודמים: {e}")

    # טבלת סימון פשוטה
    st.markdown("### סמן את המשבצות בהן אינך יכול לעבוד:")
    updated_rows = []
    for index, row in df.iterrows():
        day = row["יום"]
        cols = st.columns(len(CUSTOM_SHIFT_TIMES_PER_DAY[day]) + 1)
        cols[0].markdown(f"**{day}**")
        row_data = {"יום": day}
        for i, shift in enumerate(CUSTOM_SHIFT_TIMES_PER_DAY[day]):
            key = f"{day}_{shift}_{username}"
            checked = cols[i+1].checkbox(shift, value=row.get(shift, False), key=key)
            row_data[shift] = checked
        updated_rows.append(row_data)

    updated_df = pd.DataFrame(updated_rows)

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
        for idx, row in updated_df.iterrows():
            day = row["יום"]
            for shift in CUSTOM_SHIFT_TIMES_PER_DAY.get(day, []):
                if row.get(shift):
                    blocked.append((day, shift))

        df_save = pd.DataFrame(blocked, columns=["day", "shift"])
        df_save.to_csv(constraint_file, index=False, encoding='utf-8-sig')

        with open(note_file, "w", encoding='utf-8') as f:
            f.write(note_input)

        st.success("האילוצים נשמרו בהצלחה!")
