from flask import Flask, render_template, jsonify, request, redirect, url_for
app = Flask(__name__)



# import requests
# from bs4 import BeautifulSoup

import jwt

# 기덕님 로그인
# jwt 토큰을 만들 때 필요.
SECRET_KEY = 'FIVE'

# 회원 인증을 위한 토큰 값을 만들어 주기 위해 jwt 사용.
# jwt 2.0 이전 에는 함수의 리턴값이 '바이트 문자열'이라는 자료형이었기 때문에 뒤에 .decode('utf-8')를 붙여 일반 문자열로 바꿔줘야 했다.
# jwt 2.0 이상 버전부터는 함수의 리턴값이 일반 문자열이 되었다. 그래서 뒤에 .decode('utf-8')가 필요없어졌다.

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
# from datetime
from datetime import datetime, timedelta

# 비밀번호를 암호화 하기 위해 hashlib 라이브러리 사용.
import hashlib
# 기덕님 로그인 끝

from pymongo import MongoClient
# client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('API address', 27017, username="", password="")
client = MongoClient('localhost', 27017)
db = client.showyourbucket


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive:
        state = 'login'
    else:
        state = 'logout'
    return render_template('index.html', state=state)


@app.route('/listing', methods=['GET'])
def listing():
    buckets = list(db.bucketlist.find({}, {'_id': False}))
    return jsonify({'all_buckets': buckets})

# @app.route('/bucketdetail')
# def detail():
#     return render_template("bucketdetail.html")

@app.route('/login')
def login():

    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/posting')
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('posts.html')
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    return render_template('posts.html')

@app.route('/api/posts', methods=['POST'])
def saving_posts():
    # token_receive = request.cookies.get('mytoken') # Client 로 부터 토큰값 가져오기
    # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #jwt 토큰 받은것을 시크릿키를 가지고 복호화해서 payload에 저장하기

    title_receive = request.form['title_give']
    desc_receive = request.form['desc_give']

    file = request.files["file_give"]

    extension = file.filename.split('.')[-1]

    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title': title_receive,
        'desc': desc_receive,
        'file': f'{filename}.{extension}'
    }

    db.bucketlist.insert_one(doc)

    return jsonify({'msg':'저장이 완료되었습니다!'})

    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다!"))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 올바르지 않습니다!"))

## api rout
@app.route('/api/check_nickname', methods=['POST'])
def check_nickname():
    receive_nickname = request.form['give_nickname']
    nicknames = list(db.userinfo.find({'nickname': receive_nickname}, {'_id': False}))

    if not nicknames:
        overlap = 'pass'
    else:
        overlap = 'fail'
    return jsonify({'overlap': overlap})

@app.route('/api/check_id', methods=['POST'])
def check_id():
    receive_id = request.form['give_id']
    ids = list(db.userinfo.find({'id': receive_id}, {'_id': False}))

    if not ids:
        overlap = 'pass'
    else:
        overlap = 'fail'
    return jsonify({'overlap': overlap})

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

    db.userinfo.insert_one(doc)
    return jsonify({'msg': f'{nickname_receive}님 가입완료되었습니다:)'})

# 로그인
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.userinfo.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
