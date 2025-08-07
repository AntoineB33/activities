import requests
import json

with open('data/config.json', 'r') as f:
    config = json.load(f)

is_free = 0
if is_free:
    PROJECT_ID = config.get('PROJECT_ID_FREE')
    OUTPUT_FILE = config.get('OUTPUT_FILE_FREE')
else:
    PROJECT_ID = config.get('PROJECT_ID_SMARTTV')
    OUTPUT_FILE = config.get('OUTPUT_FILE_SMARTTV')
PRIVATE_TOKEN = config.get('PRIVATE_TOKEN')
YOUR_USERNAME = config.get('YOUR_USERNAME')

headers = {
    'PRIVATE-TOKEN': PRIVATE_TOKEN
}

base_url = f'https://gitlab.com/api/v4/projects/{PROJECT_ID}/events'

all_my_events = []
page = 1
per_page = 50
empty_my_events_count = 0  # Track consecutive empty my_events

while True:
    params = {
        'page': page,
        'per_page': per_page
    }
    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()

    events = response.json()
    if not events:
        break

    # Filter events by your username (only your activities)
    my_events = [event for event in events if event.get('author', {}).get('username') == YOUR_USERNAME]
    all_my_events.extend(my_events)

    if not my_events:
        empty_my_events_count += 1
        if empty_my_events_count >= 4:
            print(f"No events for your username found in four consecutive pages. Stopping.")
            break
    else:
        empty_my_events_count = 0

    print(f'Page {page} processed, found {len(my_events)} of your events')
    page += 1

# Save to file
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_my_events, f, indent=2)

print(f'Total your events saved: {len(all_my_events)} to {OUTPUT_FILE}')
