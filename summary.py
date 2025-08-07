import json
from datetime import datetime

STOP_AT_DATETIME = '2025-08-06 10:45'  # Change to your desired stop date and time (inclusive)
stop_at = datetime.strptime(STOP_AT_DATETIME, '%Y-%m-%d %H:%M')

# Load your activity data
with open('data/my_activities.json', 'r', encoding='utf-8') as f:
    activities = json.load(f)

# Format and print each activity
for event in activities:
    date_obj = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    if date_obj < stop_at:
        break
    date = date_obj.strftime('%Y-%m-%d %H:%M')
    action = event.get('action_name', 'did something')
    author = event.get('author', {}).get('name', 'Unknown')
    target_type = event.get('target_type', 'Unknown')
    title = event.get('target_title') or event.get('note', {}).get('body', '')[:60].replace('\n', ' ').strip()

    # Build one-line summary
    summary = f"[{date}] {author} {action} on {target_type}: {title}"
    print(summary)
