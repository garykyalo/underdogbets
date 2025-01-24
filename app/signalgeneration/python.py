

# Original datetime string
datetime_str = "2025-01-25T13:00:00Z"

# Convert to datetime object
dt = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")

# Format to the desired time
formatted_time = dt.strftime("%H:%M (UTC)")

print(formatted_time)