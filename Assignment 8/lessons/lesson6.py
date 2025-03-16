import csv

# Function to categorize magnitude descriptions
def get_magnitude_description(magnitude):
    """Returns the magnitude description based on the Richter scale."""
    if magnitude < 3.0:
        return "Micro"
    elif magnitude < 4.0:
        return "Minor"
    elif magnitude < 5.0:
        return "Light"
    elif magnitude < 6.0:
        return "Moderate"
    elif magnitude < 7.0:
        return "Strong"
    elif magnitude < 8.0:
        return "Major"
    else:
        return "Great"

# Function to process the uploaded CSV file
def process_file(file_path):
    """Processes the CSV file and returns sorted earthquake data."""
    processed_data = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                try:
                    date = row[0]
                    name = row[1]
                    magnitude = float(row[2])
                    description = get_magnitude_description(magnitude)
                    processed_data.append({
                        'date': date,
                        'name': name,
                        'magnitude': magnitude,
                        'description': description
                    })
                except ValueError:
                    continue  # Skip rows with invalid magnitude

    # Sort the data by magnitude in decreasing order
    processed_data.sort(key=lambda x: x['magnitude'], reverse=True)

    return processed_data
