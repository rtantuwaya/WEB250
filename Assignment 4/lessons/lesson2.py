# lessons/lesson2.py
from flask import render_template
import socket
import platform
from datetime import datetime

def lesson2():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = platform.system()
    os_version = platform.version()
    python_version = platform.python_version()

    return render_template('lesson2.html', current_time=current_time, hostname=hostname, ip_address=ip_address,
                           os_info=os_info, os_version=os_version, python_version=python_version)




