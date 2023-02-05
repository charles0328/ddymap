from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://charles:1111@cluster0.szvramp.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbddymap


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/board')
def board():
    count = db.board.count_documents({})
    return render_template('board.html', count=count)


@app.route('/board/regist', methods=["POST"])
def board_post():
    nickname_receive = request.form['nickname_give']
    password_receive = request.form['password_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    url_receive = request.form['url_give']

    cards_list = list(db.board.find({}, {'_id': False}))
    count = len(cards_list) + 1

    doc = {
        'num': count,
        'nickname': nickname_receive,
        'password': password_receive,
        'title': title_receive,
        'content': content_receive,
        'url': url_receive
    }
    db.board.insert_one(doc)

    return jsonify({'msg': '게시물 등록 완료!'})


@app.route('/board/regist', methods=["GET"])
def board_get():
    cards_list = list(db.board.find({}, {'_id': False}))
    return jsonify({'cards': cards_list})

@app.route('/board/regist/delete', methods=["POST"])
def card_delete():
    num_receive = request.form['num_give']
    db.board.delete_one({'num': int(num_receive)})
    return jsonify({'msg': "삭제 완료"})

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
