from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
