# utils/helpers.py

import pandas as pd
import os

SHIFT_TIMES = ["08:00-12:00", "12:00-20:00", "20:00-00:00"]
DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
SCHEDULE_FILE = "schedule.csv"

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        return pd.read_csv(SCHEDULE_FILE, index_col=0)
    else:
        positions_df = pd.read_csv("positions.csv", encoding="utf-8")
        index = []
        for pos in positions_df['position']:
            for day in DAYS:
                for shift in SHIFT_TIMES:
                    index.append(f"{pos}__{day}__{shift}")
        return pd.DataFrame(index=index, columns=["name"])

def build_schedule_table(schedule, positions_df):
    table_data = []
    for pos in positions_df['position']:
        row = {"עמדה": pos}
        for day in DAYS:
            for shift in SHIFT_TIMES:
                key = f"{day} {shift}"
                index_key = f"{pos}__{day}__{shift}"
                row[key] = schedule.loc[index_key, 'name'] if index_key in schedule.index else ""
        table_data.append(row)
    return pd.DataFrame(table_data)
