from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://charles:1111@cluster0.szvramp.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbddymap

#지도 페이지 연결
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/getdatacafe', methods=["GET"])
def data_cafe_get():
    print("data_cafe_get function called")
    cafes_count = db.cafes.count_documents({})
    print("Number of documents in cafes collection:", cafes_count)

    cafes_list = list(db.cafes.find({}, {'_id': False}))
    print("Cafes list:", cafes_list)
    return jsonify({'cafe':cafes_list})

@app.route('/getdatarefill', methods=["GET"])
def data_refill_get():
    print("data_refill_get function called")
    refills_count = db.refills.count_documents({})
    print("Number of documents in cafes collection:", refills_count)

    refills_list = list(db.refills.find({}, {'_id': False}))
    print("Refills list:", refills_list)
    return jsonify({'refill':refills_list})

@app.route('/getdatadaily', methods=["GET"])
def data_daily_get():
    print("data_daily_get function called")
    dailys_count = db.dailys.count_documents({})
    print("Number of documents in cafes collection:", dailys_count)

    dailys_list = list(db.dailys.find({}, {'_id': False}))
    print("Dailys list:", dailys_list)
    return jsonify({'daily':dailys_list})

@app.route('/getdataetc', methods=["GET"])
def data_etc_get():
    print("data_etc_get function called")
    etcs_count = db.etcs.count_documents({})
    print("Number of documents in cafes collection:", etcs_count)

    etcs_list = list(db.etcs.find({}, {'_id': False}))
    print("Etcs list:", etcs_list)
    return jsonify({'etc':etcs_list})


# 게시판 페이지 연결
@app.route('/board')
def board():
    count = db.board.count_documents({})
    return render_template('board.html', count=count)


# 게시물 DB 등록
@app.route('/board/regist', methods=["POST"])
def board_post():
    nickname_receive = request.form['nickname_give']
    password_receive = request.form['password_give']
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    url_receive = request.form['url_give']
    radio_receive = request.form['radio_give']

    cards_list = list(db.board.find({}, {'_id': False}))
    count = len(cards_list) + 1

    doc = {
        'num': count,
        'nickname': nickname_receive,
        'password': password_receive,
        'title': title_receive,
        'content': content_receive,
        'url': url_receive,
        'radio': radio_receive,
    }
    db.board.insert_one(doc)

    return jsonify({'msg': '게시물 등록 완료!'})


# 게시물 게시
@app.route('/board/regist', methods=["GET"])
def board_get():
    cards_list = list(db.board.find({}, {'_id': False}))
    return jsonify({'cards': cards_list})

# 게시물 검색
@app.route('/board/regist?=', methods=["GET"])
def search_get():
    search_receive = request.args.get('search')
    print("검색", search_receive)
    search_list = list(db.board.find({'$or': [{'title': {'$regex': search_receive}},
                                              {'content': {'$regex': search_receive}},
                                              {'nickname': {'$regex': search_receive}}]},
                                     {'_id': False}))
    print("검색 결과", search_list)
    return jsonify({'searches': search_list})


# 게시물 삭제
@app.route('/board/regist/delete', methods=["POST"])
def delete_card():

    # <!-- 삭제버튼을 누른 카드의 데이터를 가져와라-->
    num = request.form.get('num_give')
    pw = request.form.get('pw')

    # <!--DB에 저장된 카드의 'num'과 'password'를 가져와라-->
    card = db.board.find_one({'num': int(num), 'password': pw})
    print(card)
    print(num, pw)
    if card:
        db.board.delete_one({'num': int(num)})
        return jsonify({'msg': '삭제가 완료되었습니다!'})
    else:
        return jsonify({'msg': 'Card not found'}), 404


# 소개 페이지 연결
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', port=5000, debug=True)