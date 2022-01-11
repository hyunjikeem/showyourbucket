from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient
import hashlib

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


## API 부분
# 닉네임 중복 확인
@app.route('/api/check_nickname', methods=['POST'])
def check_nickname():
    receive_nickname = request.form['give_nickname']
    nicknames = list(db.user.find({'nickname': receive_nickname}, {'_id': False}))

    if not nicknames:
        overlap = 'pass'
    else:
        overlap = 'fail'
    return jsonify({'overlap': overlap})


# 아이디 중복확인
@app.route('/api/check_id', methods=['POST'])
def check_id():
    receive_id = request.form['give_id']
    ids = list(db.user.find({'id': receive_id}, {'_id': False}))

    if not ids:
        overlap = 'pass'
    else:
        overlap = 'fail'
    return jsonify({'overlap': overlap})


# 회원가입 user 정보
@app.route('/api/signup', methods=['POST'])
def signup():
    nickname_receive = request.form['give_nickname']
    id_receive = request.form['give_id']
    pw_receive = request.form['give_pw']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'nickname': nickname_receive,
        'id': id_receive,
        'pw': pw_hash,
    }

    db.user.insert_one(doc)
    return jsonify({'msg': f'{nickname_receive}님 가입완료되었습니다:)'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
