from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

import jwt

from pymongo import MongoClient
# client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('API address', 27017, username="", password="")
client = MongoClient('localhost', 27017)
db = client.bucketlist


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/main', methods=['GET'])
def listing_posts():
    buckets = list(db.bucketlist.find({}, {'_id': False}))
    return jsonify({'all_buckets': buckets})

# @app.route('/bucketdetail')
# def detail():
#     return render_template("bucketdetail.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/posting')
def posting():
    return render_template("posting.html")

# 현지님 버킷 작성하기
@app.route('/api/posts', methods=['POST'])
def saving_posts():
    # token_receive = request.cookies.get('mytoken') # Client 로 부터 토큰값 가져오기
    # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #jwt 토큰 받은것을 시크릿키를 가지고 복호화해서 payload에 저장하기

    img = request.form['img']
    title = request.form['title']
    desc = request.desc['desc']

    doc = {
        'title':title,
        'img':img,
        'desc':desc,
    }

    db.bucketlist.insert_one(doc)

    return jsonify({'msg':'저장이 완료되었습니다!'})

    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다!"))
    #
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 올바르지 않습니다!"))



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

