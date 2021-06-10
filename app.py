from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import jwt, hashlib, datetime


##################################################
# Initializing
##################################################


app = Flask(__name__)

client = MongoClient('localhost', port=27017)
db = client.dbkino


##################################################
# Routes
##################################################


@app.get('/')
def home():
    return render_template('home.html')


##################################################
# APIs
##################################################


##################################################
# Run
##################################################


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)