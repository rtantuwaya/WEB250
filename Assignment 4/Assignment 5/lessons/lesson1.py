# lessons/lesson1.py
from flask import render_template

def lesson1():
     hello_name   = "Hello, Ravindra Tantuwaya"
     return render_template('lesson1.html', hello_name  = hello_name )
