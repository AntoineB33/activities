import json
from datetime import datetime

with open('data/config.json', 'r') as f:
    config = json.load(f)

is_free = 1
if is_free:
    INPUT_FILE = config.get('INPUT_FILE_FREE')
else:
    INPUT_FILE = config.get('INPUT_FILE_SMARTTV')
STOP_AT_DATETIME = config.get('STOP_AT_DATETIME')
stop_at = datetime.strptime(STOP_AT_DATETIME, '%Y-%m-%d %H:%M')

# Load your activity data
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    activities = json.load(f)

for event in activities:
    date_obj = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if date_obj < stop_at:
        break
    date = date_obj.strftime('%Y-%m-%d %H:%M')
    author = event.get('author', {}).get('name', 'Unknown')
    action = event.get('action_name', 'did something')
    target_type = event.get('target_type', 'Unknown')

    # Title handling
    title = (
        event.get('target_title')
        or event.get('note', {}).get('body', '')[:60].replace('\n', ' ').strip()
        or event.get('push_data', {}).get('commit_title', '[No title]')
    )

    # Special handling for push events to include branch name
    if action == "pushed to" and "push_data" in event:
        branch = event["push_data"].get("ref", "unknown-branch")
        summary = f"[{date}] {author} pushed to branch '{branch}': {title}"
    else:
        # Avoid "on on" or "to on"
        if action.endswith(" on") or action.endswith(" to"):
            summary_action = f"{author} {action}"
        else:
            summary_action = f"{author} {action} on"
        summary = f"[{date}] {summary_action} {target_type}: {title}"

    print(summary)
