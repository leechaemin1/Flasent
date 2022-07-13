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


@app.route('/')
def home():
    return render_template('main.html')

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

@app.route('/post/<id>',)
def post(id):
    flower_list = list(db.flowers.find({}, {'_id': False}))
    if (int(id) >= len(flower_list)):
        return redirect('/')
    return render_template('post.html', id=id, doc=flower_list)

@app.route("/flower", methods=["GET"])
def flowers_get():
    flowers_list = list(db.flowers.find({'category': {'$regex': request.args.get('category')}},{'_id':False}))
    return jsonify({'flowers': flowers_list})

@app.route("/review", methods=["POST"])
def review_post():
    comment_receive = request.form["comment_give"]
    user_info = db.member.find_one({"username": payload["id"]})

    # doc = {
    #     "comment_list":{
    #     "username": user_info["username"],
    #     "comment": comment_receive,}
    # }
    #

    db.flowers.update(
        {"id":""}
    )

    return jsonify({'msg': '저장 완료!'})

@app.route("/review", methods=["GET"])
def review_get():
    comment_list = list(db.flowers.find({},{'_id':False}))
    user_info = db.member.find_one({"username": payload["id"]})
    return jsonify({'comments':comment_list, 'info':user_info})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
