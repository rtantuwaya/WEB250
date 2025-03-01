# from flask import Flask, render_template, request
# import csv
# import io



# Function to convert km/h to mph
def kmh_to_mph(kmh):
    return kmh * 0.621371

# Function to determine Saffir-Simpson scale category
def get_saffir_simpson_category(wind_speed_kmh):
    mph = kmh_to_mph(wind_speed_kmh)
    if mph < 74:
        return "Tropical Storm", "category-1"
    elif 74 <= mph <= 95:
        return "Category 1", "category-1"
    elif 96 <= mph <= 110:
        return "Category 2", "category-2"
    elif 111 <= mph <= 129:
        return "Category 3", "category-3"
    elif 130 <= mph <= 156:
        return "Category 4", "category-4"
    else:
        return "Category 5", "category-5"



