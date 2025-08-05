import streamlit as st
import pandas as pd
import os
from utils.helpers import SHIFT_TIMES, DAYS

CONSTRAINT_DIR = "constraints"

def show_constraints_tab(username):
    st.subheader("🚫 סימון אילוצים לשבוע הבא")

    # Load positions
    positions_df = pd.read_csv("positions.csv", encoding='utf-8')
    positions = positions_df['position'].tolist()

    # Load existing constraints if available
    os.makedirs(CONSTRAINT_DIR, exist_ok=True)
    constraint_file = os.path.join(CONSTRAINT_DIR, f"{username}_constraints.csv")
    note_file = os.path.join(CONSTRAINT_DIR, f"{username}_note.txt")

    if os.path.exists(constraint_file):
        constraints_df = pd.read_csv(constraint_file)
        marked = set(tuple(row) for row in constraints_df.values)
    else:
        marked = set()

    # Build grid with ❌ buttons
    st.markdown("### סמן את המשבצות בהן אינך יכול לעבוד:")
    for pos in positions:
        st.markdown(f"#### עמדה: {pos}")
        for day in DAYS:
            cols = st.columns(len(SHIFT_TIMES))
            for i, shift in enumerate(SHIFT_TIMES):
                key = f"{pos}__{day}__{shift}"
                is_marked = (pos, day, shift) in marked
                if cols[i].button("❌" if is_marked else "⬜", key=key):
                    if is_marked:
                        marked.remove((pos, day, shift))
                    else:
                        marked.add((pos, day, shift))

    # Note box
    st.markdown("### הערה למנהל (לא חובה):")
    note = ""
    if os.path.exists(note_file):
        with open(note_file, "r", encoding='utf-8') as f:
            note = f.read()
    note_input = st.text_area("הקלד הערה", value=note)

    # Save button
    if st.button("💾 שמור אילוצים"):
        df = pd.DataFrame(marked, columns=["position", "day", "shift"])
        df.to_csv(constraint_file, index=False, encoding='utf-8-sig')
        with open(note_file, "w", encoding='utf-8') as f:
            f.write(note_input)
        st.success("האילוצים נשמרו בהצלחה!")
