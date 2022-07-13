from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import jwt
import hashlib
import datetime

app = Flask(__name__)

from pymongo import MongoClient
import certifi

client = MongoClient('mongodb+srv://diana:sparta@cluster0.oscy4t6.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=certifi.where())
db = client.flower

SECRET_KEY = 'SPARTA'


@app.route('/', methods=["GET"])
def home():
    category_receive = request.args.get('category_give')
    print(category_receive)
    flower_list = list(db.flowers.find({}, {'_id': False}))
    # for f_list in flower_list:
    #     if category_receive is None:
    #         print('afdsfsdf')
    #     if category_receive in f_list['category']:
    #         print('cate', category_receive, 'f_list', f_list)
    return render_template('main.html', lists=flower_list)

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/membership')
def membership():
    return render_template('membership.html')

@app.route('/post/<id>')
def post(id):
    flower_list = list(db.flowers.find({}, {'_id': False}))
    if (int(id) >= len(flower_list)):
        return redirect('/')
    return render_template('post.html', id=id, doc=flower_list)



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
