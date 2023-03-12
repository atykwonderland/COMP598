from flask import Flask, jsonify
import sys
import random
import string

app = Flask(__name__)

@app.route('/register/<name>/<pod_name>')
def register_node(name, pod_name):
   
    
    
