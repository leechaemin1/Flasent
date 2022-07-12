import json

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://diana:sparta@cluster0.oscy4t6.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=certifi.where())
db = client.flower


@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/membership')
def membership():
    return render_template('membership.html')

@app.route('/post/<id>')
def post(id):
    flower_list = list(db.flowers.find({}, {'_id': False}))
    print(flower_list)
    return render_template('post.html', id=id, doc=flower_list)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
