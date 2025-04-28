# data_store.py

def initialize_store():
    """
    Initializes and returns a new, empty data store and ID counter.
    """
    return {}, 1  # wildfire_data, next_id

def insert_record(wildfire_data, next_id, name, location, date_str, severity):
    try:
        severity = int(severity)
    except (ValueError, TypeError):
        severity = 0  # or handle differently
    wildfire_data[next_id] = {
        "id": next_id,
        "name": name,
        "location": location,
        "date": date_str,
        "severity": severity
    }
    return wildfire_data, next_id + 1


def update_record(wildfire_data, record_id, name, location, date_str, severity):
    try:
        severity = int(severity)
    except (ValueError, TypeError):
        severity = 0  # or handle differently
    if record_id in wildfire_data:
        wildfire_data[record_id] = {
            "id": record_id,
            "name": name,
            "location": location,
            "date": date_str,
            "severity": severity
        }
    return wildfire_data


def delete_record(wildfire_data, record_id):
  
    wildfire_data.pop(record_id, None)
    return wildfire_data

def get_all_records(wildfire_data):
    
    return list(wildfire_data.values())
