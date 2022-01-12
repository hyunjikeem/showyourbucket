from flask import Flask, render_template, jsonify, request, redirect, url_for

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta

from datetime import datetime

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():


    return jsonify({'all_articles': articles})


## API 역할을 하는 부분
@app.route('/api/posts', methods=['POST'])
def saving_posts():
    # token_receive = request.cookies.get('mytoken') # Client 로 부터 토큰값 가져오기
    # payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256']) #jwt 토큰 받은것을 시크릿키를 가지고 복호화해서 payload에 저장하기

    # img = request.form['img']
    # title = request.form['title']
    # desc = request.form['desc']

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
        'title':title_receive,
        'desc':desc_receive,
        'file': f'{filename}.{extension}'
    }

    # doc = {
    #     'title': title,
    #     'img': img,
    #     'desc': desc,
    # }

    db.bucketlist.insert_one(doc)

    return jsonify({'msg':'저장이 완료되었습니다!'})

    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다!"))
    #
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 올바르지 않습니다!"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)