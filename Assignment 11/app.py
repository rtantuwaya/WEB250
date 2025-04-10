from flask import Flask, render_template, request, redirect, url_for, jsonify
import socket
import platform
import pymongo
from lessons.lesson1 import lesson1
from lessons.lesson2 import lesson2
from lessons.lesson3 import convert_units
from datetime import datetime
from lessons.lesson4 import start_game, check_answer 
import csv
import io
import os
import sqlite3
from lessons.lesson5 import kmh_to_mph, get_saffir_simpson_category
from lessons.lesson6 import process_file
from lessons.lesson7 import uploadfile, parse_csv, get_impact_color  # Import functions from lesson7.py
from lessons.lesson8 import fetch_storm_data # Import functions from lesson8.py
from lessons.lesson9 import get_db_connection, init_db, get_records
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from lessons.lesson10 import index10, addMongo_record, updateM_record, delete_record
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from lessons.lesson11 import db, User, init_db


app = Flask(__name__)

# MongoDB client setup

app.config["MONGO_URI"] = "mongodb://mongodb:27017/weatherDB"
mongo = PyMongo(app)
app.secret_key = 'your_secret_key'  # Replace with your actual secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


init_db(app)



# Home route for the course website
@app.route('/')
def home():
    return render_template('index.html')

# Route for Lesson 1 (Hello_name)

# Lesson 1 route
@app.route('/lesson1')
def lesson1_route():
    return lesson1()  # Call the function, not the module


# Route for Lesson 2 (Server information)

@app.route('/lesson2')
def lesson2_route():
    return lesson2()

#Assignment 3

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    result = None
    if request.method == 'POST':
        value = float(request.form['value'])
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        result = convert_units(value, from_unit, to_unit)
    return render_template('unit_converter.html', result=result)
#Assignment 4

# Route to handle the start of the game and form submission

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
         # Retrieve the base value and number of expressions from the form
        value = request.form.get("value")
        expressions = request.form.get("expressions")

           # Debug print statements to verify the form data
        print(f"Received value: {value}, expressions: {expressions}")

             # Check if both parameters are provided
        if not value or not expressions:
            return "Missing value or expressions parameter", 400
        
         # Redirect to the /game route with the query parameters
        return redirect(url_for("game", value=value, expressions=expressions))
    
    return render_template("index4.html")


# Route to display the math problems

@app.route("/game")
def game():
 # Get the query parameters from the URL
    value = request.args.get("value")
    expressions = request.args.get("expressions")

      # Debugging print statements to verify query parameters
    print(f"Received value: {value}, expressions: {expressions}")
    
    # Ensure the parameters are provided
    if not value or not expressions:
        return "Error: Missing value or expressions parameter", 400
    
      # Convert them to integers
    value = int(value)
    expressions = int(expressions)

    # Call the start_game function from lesson4.py
    game_data = start_game(value, expressions)

    return render_template("game.html", value=value, expressions=expressions, game_data=game_data)




# Route to process the user's answer
@app.route("/check_answer", methods=["POST"])
def check_answer_route():
    user_answer = int(request.form["user_answer"])  # User's answer
    correct_answer = int(request.form["correct_answer"])  # The correct answer for the current question
    
    # Call the check_answer function from lesson4.py
    result = check_answer(user_answer, correct_answer)

    # Redirect back with the result
    return redirect(url_for("game_result", result=result))

# Route to show the result after checking
@app.route("/result")
def game_result():
    result = request.args.get("result", "")  # Retrieve result (Correct or Incorrect)
    return render_template("result.html", result=result)

#Assignment 5

# Route for uploading and processing CSV
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    data = []
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            # Read the uploaded CSV file
            content = file.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(content), delimiter=',')
            
            for row in csv_reader:
                print("Row:", row)  # Print each row to verify CSV parsing

                # Assuming the CSV structure is: Date, Storm Name, Max Winds (km/h)
                if len(row) != 3:
                    print(f"Skipping row (incorrect structure): {row}")
                    continue  # Skip rows that don't match expected structure

                date, storm_name, winds_kmh = row
                try:
                    winds_kmh = float(winds_kmh)
                except ValueError:
                    print(f"Skipping row (invalid wind speed): {row}")
                    continue  # Skip invalid wind speed values

                category, category_class = get_saffir_simpson_category(winds_kmh)
                data.append({
                    'date': date,
                    'storm_name': storm_name,
                    'winds_kmh': winds_kmh,
                    'winds_mph': kmh_to_mph(winds_kmh),
                    'category': category,
                    'category_class': category_class
                })

    return render_template('index5.html', data=data)

#Assignment 6

# Path to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index6')
def index6():
    """Render the upload form."""
    return render_template('index6.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle the uploaded file, process it, and display the results."""
    # Check if the file part is in the request
    if 'earthquakeFile' not in request.files:
        return 'No file part', 400

    file = request.files['earthquakeFile']

    # If no file is selected
    if file.filename == '':
        return 'No selected file', 400

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Process the uploaded file and get sorted earthquake data
    processed_data = process_file(file_path)

    # Render the result template with the processed data
    return render_template('result6.html', earthquakes=processed_data)

    #Assignment 7

@app.route("/lesson7", methods=["GET", "POST"])
def index7():
    wildfires = []

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            # print(f"Received file: {file.filename}")  # Debugging
            file_path = uploadfile(file)
            wildfires = parse_csv(file_path)

            # Sort the wildfires array by area impacted in descending order
            wildfires.sort(key=lambda x: x['area_impacted'], reverse=True)
    # else:print("No file uploaded.")  # Debugging
    return render_template("index7.html", wildfires=wildfires, get_impact_color=get_impact_color)
 
 #Assignment 8 
 
@app.route('/lesson8')
def index8():
    storms = fetch_storm_data()  # Fetch and process storm data from storm_data.py
    return render_template('lesson8.html', storms=storms)


#Assignment 9
# Assignment 9 (Database Interaction)
# Manually call init_db on startup to initialize the database

# def initialize():
 #    init_db(app)  Initialize the database (creates the records table if not exi

# Call initialize() before running the app to make sure the database is set up
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# initialize()

@app.route('/index9')
def index9():
    records = get_records()  # Fetch records from the database
    return render_template('index9.html', records=records)

# Add a new record to the database
@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    created_at = request.form['created_at']
    conn = get_db_connection()
    conn.execute('INSERT INTO records (name, email, age, created_at) VALUES (?, ?, ?, ?)',
                 (name, email, age, created_at))
    conn.commit()
    conn.close()
    return redirect(url_for('index9'))

# Update an existing record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_record(id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        created_at = request.form['created_at']
        conn.execute('UPDATE records SET name = ?, email = ?, age = ?, created_at = ? WHERE id = ?',
                     (name, email, age, created_at, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index9'))
    record = conn.execute('SELECT * FROM records WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('update.html', record=record)

# Delete an existing record
@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index9'))

#Assignment 10
app.secret_key = "your_secret_key"  # For flashing messages

# Another route example (you can add more)
@app.route('/users')
def users():
    users = mongo.db.users.find()  # Query MongoDB
    return f"Users: {users}"

# Home route to display records
@app.route('/index10_route')
def index10_route():
    return index10(mongo)  # Call the index10 function with mongo as a parameter

# Route to add new record
@app.route('/addMongo', methods=['POST'])
def addMongo():
    return addMongo_record(mongo)

# Route to update an existing record
@app.route('/updateM/<record_id>', methods=['POST'])
def updateM(record_id):
    return updateM_record(mongo, record_id)

# Route to delete a record
@app.route('/delete/<record_id>', methods=['GET'])
def delete(record_id):
    return delete_record(mongo, record_id)

#Assignment 11



# Initialize the database 



# @app.route('/')
# def home():
@app.route('/lesson11') 
def lesson11_route():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))
#---test---

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check for empty fields
        if not username or not password:
            flash('Please fill in both fields.', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('login.html')

# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Both username and password are required!', 'danger')
            return redirect(url_for('register'))
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken, please choose another.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

#--test---

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#Assignment 11

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
# app.run(host='0.0.0.0', port=5000)
# app.run(debug=True)


