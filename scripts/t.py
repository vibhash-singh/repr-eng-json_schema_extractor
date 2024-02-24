from datetime import datetime

# Parse the start and end timestamps
start = datetime.fromisoformat('2024-02-21T22:37:24.517Z')
end = datetime.fromisoformat('2024-02-21T22:37:36.550Z')

# Calculate the duration in seconds
duration_seconds = (end - start).total_seconds()
duration_seconds