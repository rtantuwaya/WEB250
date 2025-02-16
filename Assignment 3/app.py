from flask import Flask, render_template, request
import socket
import platform
from lessons.lesson1 import hello_name  # hello_name()
from lessons.lesson2 import lesson2_content
from datetime import datetime

app = Flask(__name__)

# Home route for the course website
@app.route('/')
def home():
    return render_template('index.html')

# Route for Lesson 1 (Hello_name)

@app.route('/lesson1')
def lesson1():
     return render_template('lesson1.html', hello_name=hello_name())


# Route for Lesson 2 (Server information)

@app.route('/lesson2')
def lesson2():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = platform.system()
    os_version = platform.version()
    python_version = platform.python_version()

    return render_template('lesson2.html', current_time=current_time, hostname=hostname, ip_address=ip_address,
                           os_info=os_info, os_version=os_version, python_version=python_version)
#Assignment 3
def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        'meters': 1,
        'kilometers': 1000,
        'miles': 1609.34
    }

    if from_unit == to_unit:
        return value

    value_in_meters = value * conversion_factors[from_unit]
    result = value_in_meters / conversion_factors[to_unit]
    return result

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    result = None
    if request.method == 'POST':
        value = float(request.form['value'])
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        result = convert_units(value, from_unit, to_unit)
    return render_template('unit_converter.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
