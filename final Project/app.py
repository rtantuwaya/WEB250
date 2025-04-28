from flask import Flask, render_template, request, redirect, url_for
from lessons.lesson1 import lesson1
from lessons.lesson2 import lesson2
from lessons.lesson3 import convert_units
from lessons.lesson4 import start_game, check_answer 
import csv
import io
import os
from lessons.lesson5 import kmh_to_mph, get_saffir_simpson_category
from lessons.lesson6 import process_file
from lessons.lesson7 import uploadfile, parse_csv, get_impact_color  # Import functions from lesson7.py
from lessons.lesson8 import fetch_storm_data 
from lessons.lesson9 import get_db_connection, init_db, get_records
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash
from lessons.lesson11 import user_list, get_user_by_username, add_user
from lessons.lesson12 import initialize_store, insert_record, update_record, delete_record, get_all_records

import sqlite3

app = Flask(__name__)
# app = Flask(__name__, static_folder='static')

# Home route for the course website
@app.route('/')
def home():
    return render_template('index.html')

# Route for Lesson 1 (Hello_name)
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
@app.route("/index4", methods=["GET", "POST"])
def index4():
    if request.method == "POST":
        value = request.form.get("value")
        expressions = request.form.get("expressions")
        print(f"Received value: {value}, expressions: {expressions}")
        if not value or not expressions:
            return "Missing value or expressions parameter", 400
        return redirect(url_for("game", value=value, expressions=expressions))
    return render_template("index4.html")


@app.route("/game")
def game():
    value = request.args.get("value")
    expressions = request.args.get("expressions")
    print(f"Received value: {value}, expressions: {expressions}")
    if not value or not expressions:
        return "Error: Missing value or expressions parameter", 400
    value = int(value)
    expressions = int(expressions)
    game_data = start_game(value, expressions)
    return render_template("game.html", value=value, expressions=expressions, game_data=game_data)

@app.route("/check_answer", methods=["POST"])
def check_answer_route():
    user_answer = int(request.form["user_answer"])  
    correct_answer = int(request.form["correct_answer"]) 
    result = check_answer(user_answer, correct_answer)
    return redirect(url_for("game_result", result=result))

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
            content = file.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(content), delimiter=',')
            for row in csv_reader:
                print("Row:", row)  
                if len(row) != 3:
                    print(f"Skipping row (incorrect structure): {row}")
                    continue  
                date, storm_name, winds_kmh = row
                try:
                    winds_kmh = float(winds_kmh)
                except ValueError:
                    print(f"Skipping row (invalid wind speed): {row}")
                    continue  

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
    if 'earthquakeFile' not in request.files:
        return 'No file part', 400
    file = request.files['earthquakeFile']
    if file.filename == '':
        return 'No selected file', 400
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    processed_data = process_file(file_path)
    return render_template('result6.html', earthquakes=processed_data)

    #Assignment 7

@app.route("/lesson7", methods=["GET", "POST"])
def index7():
    wildfires = []
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            file_path = uploadfile(file)
            wildfires = parse_csv(file_path)
            wildfires.sort(key=lambda x: x['area_impacted'], reverse=True)
    return render_template("index7.html", wildfires=wildfires, get_impact_color=get_impact_color)
 
 #Assignment 8 
 
@app.route('/lesson8')
def index8():
    storms = fetch_storm_data()  # Fetch and process storm data from storm_data.py
    return render_template('lesson8.html', storms=storms)

#Assignment 9

init_db()
@app.route('/index9')
def index9():
    records = get_records()  # Fetch records from the database
    return render_template('index9.html', records=records)

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
""" app.secret_key  """

#Assignment 11

app.secret_key = os.urandom(32)

@app.route('/lesson11') 
def lesson11_route():
    if 'username' in session:
        return render_template('home11.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if get_user_by_username(username):
            flash('Username already exists. Please choose a different one.', 'warning')
            return redirect(url_for('register'))

        add_user(username, password)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

#Assignment 12

wildfire_data, next_id = initialize_store()

@app.route('/lesson12', methods=['GET', 'POST']) 
def index12():
    global wildfire_data, next_id
    if request.method == "POST":
        action = request.form.get("action")
        name = request.form.get("name")
        location = request.form.get("location")
        date_str = request.form.get("date")
        severity = request.form.get("severity")
        id_str = request.form.get("id")
        
        if action in ["Update", "Delete"]:
            if not id_str or not id_str.isdigit():
                flash("Invalid or missing record ID.", "danger")
                return redirect("/lesson12")
            record_id = int(id_str)

        if action == "Insert":
            wildfire_data, next_id = insert_record(wildfire_data, next_id, name, location, date_str, severity)
        elif action == "Update":
            wildfire_data = update_record(wildfire_data, record_id, name, location, date_str, severity)
        elif action == "Delete":
            wildfire_data = delete_record(wildfire_data, record_id)

        return redirect("/lesson12")

    records = get_all_records(wildfire_data)
    return render_template("index12.html", records=records)


@app.route('/lesson14')
def lesson14():
    return render_template('index14.html')

@app.route('/FinalProject')
def FinalProject():
    return render_template('finalindex.html')

if __name__ == '__main__':
    
 app.run(host="0.0.0.0", port=5000, debug=True)



 