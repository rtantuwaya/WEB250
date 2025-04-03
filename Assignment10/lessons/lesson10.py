from flask import render_template, request, redirect, url_for, flash
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient

# Home route to display records
client = MongoClient("mongodb://mongodb:27017/weatherDB")  # Use the container name `mongodb` here
db = client.weatherDB


def index10(mongo):
    records = mongo.db.records.find()
    return render_template('index10.html', records=records)

# Route to add new record
def addMongo_record(mongo):
    description = request.form.get('description')
    severity = request.form.get('severity')
    
    if not description or not severity:
        flash("Description and severity are required!", "error")
        return redirect(url_for('home'))

    try:
        date = datetime.now()
        mongo.db.records.insert_one({
            "description": description,
            "severity": int(severity),
            "date": date
        })
        flash("Record added successfully!", "success")
    except Exception as e:
        flash(f"Error adding record: {e}", "error")

    return redirect(url_for('home'))

# Route to update an existing record
def updateM_record(mongo, record_id):
    description = request.form.get('description')
    severity = request.form.get('severity')

    if not description or not severity:
        flash("Description and severity are required!", "error")
        return redirect(url_for('home'))

    try:
        mongo.db.records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {"description": description, "severity": int(severity)}}
        )
        flash("Record updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating record: {e}", "error")

    return redirect(url_for('home'))

# Route to delete a record
def delete_record(mongo, record_id):
    try:
        mongo.db.records.delete_one({"_id": ObjectId(record_id)})
        flash("Record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "error")

    return redirect(url_for('home'))
