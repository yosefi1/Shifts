import streamlit as st
import pandas as pd
from datetime import date

FILENAME = "constraints.csv"

st.set_page_config(page_title="ניהול אילוצים לשמירה", layout="centered")

st.title("🛡️ הזנת אילוצים למשמרות")

# הזדהות פשוטה (שלב ראשון בלבד)
name = st.text_input("הכנס את שמך")

# רק אם יש שם – מציגים טופס
if name:
    st.subheader("הזן אילוצים לשבוע הקרוב:")

    unavailable_days = st.multiselect(
        "באילו ימים אינך יכול לעבוד?",
        ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
    )

    comment = st.text_area("הערות נוספות")

    if st.button("שמור"):
        new_entry = {
            "שם": name,
            "תאריך שליחה": date.today().isoformat(),
            "ימים חסומים": ", ".join(unavailable_days),
            "הערות": comment
        }

        try:
            df = pd.read_csv(FILENAME)
        except FileNotFoundError:
            df = pd.DataFrame(columns=new_entry.keys())

        df = df.append(new_entry, ignore_index=True)
        df.to_csv(FILENAME, index=False)
        st.success("הבקשה נשמרה בהצלחה ✅")

    # הצגת הנתונים (למנהל)
    st.subheader("📋 כל האילוצים שהוזנו עד כה")
    try:
        df = pd.read_csv(FILENAME)
        st.dataframe(df)
    except:
        st.info("עדיין לא הוזנו אילוצים.")
else:
    st.warning("נא להזין שם כדי להמשיך")
