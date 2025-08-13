import json
import sys
from collections import OrderedDict

# Change this path if needed
INPUT_FILE = "data/my_activities_free.json"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        activities = json.load(f)

    seen = OrderedDict()
    for event in activities:
        action = event.get("action_name", "")
        if action in ("pushed to", "pushed new") and "push_data" in event:
            branch = event["push_data"].get("ref")
            if branch and branch not in seen:
                seen[branch] = None

    print("Branches you worked in (in order of apparition):")
    for branch in seen:
        print(branch)

if __name__ == "__main__":
    main()
