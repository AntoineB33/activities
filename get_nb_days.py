import re
import pandas as pd
import pyperclip

# Get text from clipboard
text = pyperclip.paste()

# Extract dates with regex
matches = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", text)
if len(matches) < 2:
    raise ValueError("Could not find two datetime strings in clipboard.")

# Convert to pandas datetime
start = pd.to_datetime(matches[0])
end = pd.to_datetime(matches[1])

# Calculate number of business days (excluding weekends)
# +1 if you want to include the start date itself
business_days = pd.bdate_range(start, end).size

# Put result back to clipboard
pyperclip.copy(str(business_days))

print(f"Number of working days between {start} and {end}: {business_days}")
