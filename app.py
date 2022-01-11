from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


## api rout
@app.route('/api/check_nickname', methods=['POST'])
def check_nickname():
    receive_nickname = request.form['give_nickname']
    nicknames = list(db.showbuket.find({'nickname': receive_nickname}, {'_id': False}))

    if not nicknames:
        overlap = 'pass'
    else:
        overlap = 'fail'
    return jsonify({'overlap': overlap})


@app.route('/api/check_id', methods=['POST'])
def check_id():
    receive_id = request.form['give_id']
    ids = list(db.showbuket.find({'id': receive_id}, {'_id': False}))

    if not ids:
        overlap = 'pass'
    else:
        overlap = 'fail'
    return jsonify({'overlap': overlap})


@app.route('/api/signup', methods=['POST'])
def signup():
    receive_nickname = request.form['give_nickname']
    receive_id = request.form['give_id']
    receive_pw = request.form['give_pw']
    receive_repw = request.form['give_repw']
    doc = {
        'nickname': receive_nickname,
        'id': receive_id,
        'pw': receive_pw,
        'repw': receive_repw
    }
    print(doc)
    db.showbuket.insert_one(doc)
    return jsonify({'msg': f'{receive_nickname}님 가입완료되었습니다:)'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
