import serial
import json
import threading, time
from flask import Flask, request, render_template
from flask_cors import CORS

ser = serial.Serial("COM9", 9600)
lm75a_str = b''

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def hello():
    res = json.dumps({'lm75a': str(lm75a_str)})
    return res

def worker():
    global lm75a_str
    while True:
        lm75a_str = ser.readline().split(b'\r\n')[0].decode("utf-8")
        print("ПОКАЗАТЕЛЬ lm75a: " + lm75a_str)
        time.sleep(0.1)

thread = threading.Thread(target=worker)
thread.start()
app.run(host='localhost', port=5001)
thread.join()
#комментарий