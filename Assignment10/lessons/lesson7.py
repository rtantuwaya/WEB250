import os
import csv

# Constants for the area impact thresholds
AREA_THRESHOLD_1 = 1
AREA_THRESHOLD_10 = 10
AREA_THRESHOLD_100 = 100
AREA_THRESHOLD_1000 = 1000

# Function to handle file upload
def uploadfile(file):
    # Directory to store uploaded files
    upload_folder = 'uploads/'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path

# Function to parse the CSV file and return an array of wildfires
def parse_csv(file_path):
    wildfires = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            try:
                # Assuming the CSV contains Date, Wildfire Name, Area Impacted
                wildfire = {
                    'date': row[0],
                    'wildfire_name': row[1],
                    'area_impacted': int(row[2])  # Convert the area impacted to integer
                }
                wildfires.append(wildfire)
            except ValueError:
                # Handle the case where the 'area_impacted' is not an integer
                print(f"Skipping row due to invalid data: {row}")
                continue

    return wildfires

# Function to determine the background color based on area impacted
def get_impact_color(area_impacted):
    if area_impacted >= AREA_THRESHOLD_1000:
        return '#FF0000'  # Red for large impact
    elif area_impacted >= AREA_THRESHOLD_100:
        return '#FF8000'  # Orange for medium-high impact
    elif area_impacted >= AREA_THRESHOLD_10:
        return '#FFFF00'  # Yellow for medium impact
    else:
        return '#00FF00'  # Green for low impact
