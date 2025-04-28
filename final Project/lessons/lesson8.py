# storm_data.py

# Constants for wind thresholds (in mph)
CATEGORY_1_THRESHOLD = 74
CATEGORY_2_THRESHOLD = 96
CATEGORY_3_THRESHOLD = 111
CATEGORY_4_THRESHOLD = 131
CATEGORY_5_THRESHOLD = 157

# Convert km/h to mph
def kmh_to_mph(kmh):
    return round(kmh * 0.621371, 2)

# Determine the Saffir-Simpson category
def get_category(windSpeedKmh):
    windSpeedMph = kmh_to_mph(windSpeedKmh)
    if windSpeedMph >= CATEGORY_5_THRESHOLD:
        return 5
    elif windSpeedMph >= CATEGORY_4_THRESHOLD:
        return 4
    elif windSpeedMph >= CATEGORY_3_THRESHOLD:
        return 3
    elif windSpeedMph >= CATEGORY_2_THRESHOLD:
        return 2
    elif windSpeedMph >= CATEGORY_1_THRESHOLD:
        return 1
    return 0  # Tropical Storm

# Fetch and process storm data
def fetch_storm_data():
    # Here we simulate the JSON data. You can replace this with an actual API request if needed.
    storm_data = [
        {"name": "Storm A", "date": "2023-07-01", "maxWindKmh": 120},
        {"name": "Storm B", "date": "2023-08-12", "maxWindKmh": 85},
        {"name": "Storm C", "date": "2023-06-20", "maxWindKmh": 180}
    ]
    
    # Process the data
    storms = []
    for storm in storm_data:
        max_wind_mph = kmh_to_mph(storm["maxWindKmh"])
        category = get_category(storm["maxWindKmh"])
        storms.append({
            "name": storm["name"],
            "date": storm["date"],
            "maxWindKmh": storm["maxWindKmh"],
            "maxWindMph": max_wind_mph,
            "category": category
        })

    # Sort by maxWindKmh in descending order
    storms.sort(key=lambda x: x['maxWindKmh'], reverse=True)
    return storms
