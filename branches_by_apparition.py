import json
import sys
from collections import defaultdict
from dateutil import parser
import pytz

# Change this path if needed
INPUT_FILE = "data/my_activities_free.json"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        activities = json.load(f)

    # branch -> list of dates
    branch_dates = defaultdict(list)
    paris_tz = pytz.timezone("Europe/Paris")

    for event in activities:
        action = event.get("action_name", "")
        if action in ("pushed to", "pushed new") and "push_data" in event:
            push_data = event["push_data"]
            branch = push_data.get("ref")
            if branch:
                branch_dates[branch].append(event["created_at"])

    # Print first and last date for each branch (in France time)
    branches_with_dates = []

    for branch, dates in branch_dates.items():
        sorted_dates = sorted(dates)
        first_utc = parser.isoparse(sorted_dates[0]).astimezone(paris_tz)
        last_utc = parser.isoparse(sorted_dates[-1]).astimezone(paris_tz)
        branches_with_dates.append((branch, first_utc, last_utc))

    # Sort by first date, newest first
    branches_with_dates.sort(key=lambda x: x[1], reverse=True)

    for branch, first_dt, last_dt in branches_with_dates:
        print(f"{branch}: first={first_dt.strftime('%Y-%m-%d %H:%M:%S')}, last={last_dt.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
