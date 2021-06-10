from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt, hashlib, os
import datetime

##################################################
# Initializing
##################################################


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

client = MongoClient('localhost', port=27017)
db = client.dbkino

##################################################
# Variables, Functions
##################################################
SECRET_KEY = "SPARTA"


def decode_token():
    token = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_find = db.users.find_one({'user_id': payload['id']})
        if user_find is not None:
            return {"result": "success", "data": payload['id']}
        else:
            return {"result": "failed", "msg": "유효하지 않은 사용자입니다."}
    except jwt.ExpiredSignatureError:
        return {"result": "failed", "msg": "로그인 시간이 만료되었습니다."}
    except jwt.DecodeError:
        return {"result": "failed", "msg": "로그인 정보가 존재하지 않습니다."}


##################################################
# Routes
##################################################


@app.get('/')
def home():
    decoded = decode_token()
    if decoded['result'] != 'success':
        return render_template('home.html', token_err_msg=decoded['msg'])

    user_info = db.users.find_one({'user_id': decoded['data']}, {'_id': False})

    return render_template('home.html', page_name="home", user_info=user_info)


@app.get('/detail')
def detail():
    decoded = decode_token()
    if decoded['result'] != 'success':
        return render_template('detail.html', token_err_msg=decoded['msg'])

    user_id = decoded['data']
    movie_id = request.args.get('id')

    movie_info = db.movies.find_one({'movie_id': movie_id}, {'_id': False})
    user_info = db.users.find_one({'user_id': user_id}, {'_id': False})
    reviews = list(db.reviews.find({'review_movie': movie_id}, {'_id': False}))

    review = db.reviews.find_one({"$and": [{"review_user": user_id}, {"review_movie": movie_id}]}, {'_id': False})

    review_exist = False

    if review is not None:
        review_exist = True

    return render_template('detail.html', page_name="detail", my_review=review, reviews=reviews, movie_info=movie_info, user_info=user_info, review_exist=review_exist)

    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     receive_id = request.args.get("id")
    #     user_info = db.reviews.find_one({'review_user': payload['id']}, {'_id': False})
    #     user_data = db.users.find_one({'user_id': payload['id']}, {'_id':False})
    #     if user_info is not None:
    #         movies = list(db.movies.find({'movie_id': receive_id}, {'_id': False}))
    #         image = db.movies.find_one({'movie_id': receive_id})['movie_img']
    #         reviews = list(db.reviews.find({'review_movie': receive_id}, {'_id': False}))
    #         reviews.reverse()
    #         review_exist = True
    #     elif user_info is None:
    #         movies = list(db.movies.find({'movie_id': receive_id}, {'_id': False}))
    #         image = db.movies.find_one({'movie_id': receive_id})['movie_img']
    #         reviews = list(db.reviews.find({'review_movie': receive_id}, {'_id': False}))
    #         reviews.reverse()
    #         review_exist = False
    #     return render_template('detail.html', movies=movies, image=image, reviews=reviews, receive_id=receive_id,
    #                            user_id=payload['id'], review_exist=False, user_info=user_data, page_name="detail")
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.get("/user")
def user():
    decoded = decode_token()
    if decoded['result'] != 'success':
        return render_template('user.html', token_err_msg=decoded['msg'])

    # query에서 유저ID 가져오기
    user_id = request.args.get('id')

    # 유저가 아니면 home으로..
    if user_id is None:
        return redirect(url_for('home'))

    # 유저ID로 DB에 있는 유저정보 검색
    user_info = db.users.find_one({'user_id': user_id}, {'_id': False})

    # 유저ID로 DB에 있는 리뷰 data 검색
    reviews = list(db.reviews.find({'review_user': user_id}, {'_id': False}))

    # 리뷰 data에서 얻은 영화ID로 DB에 있는 영화이름 검색
    # 찾은 영화이름을 리뷰 data에 추가
    if reviews is not None:
        for review in reviews:
            review.update(db.movies.find_one({'movie_id': review['review_movie']}, {'_id': False, 'movie_title': True}))

    # 유저정보와 리뷰 data 리스트를 html에 전달.
    return render_template("user.html", user_info=user_info, reviews=reviews, page_name="user")


@app.get("/login")
def login():
    decoded = decode_token()
    if decoded['result'] == 'success':
        return redirect(url_for('home'))
    return render_template('login.html')


##################################################
# APIs
##################################################

@app.get('/movies')
def show_movies():
    movie_list = list(db.movies.find({}, {'_id': False}))
    for movie in movie_list:
        movie_id = movie['movie_id']
        review_list = list(db.reviews.find({'review_movie': movie_id}))
        star_sum = 0
        if len(review_list) != 0:
            for review in review_list:
                star_sum += int(review['review_star'])
            star_avg = star_sum / len(review_list)
            movie['star_avg'] = star_avg
        else:
            movie['star_avg'] = 0
    #   movie_list[i]['star_avg'] = star_avg

    kino_rank = 0
    for i in movie_list:
        kino_rank += 1
        i['kino_rank'] = kino_rank
    #   movie_list[i]['star_avg'] = star_avg

    return jsonify({'movie_list': movie_list})



@app.post("/api/login")
def login_api():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'user_id': username_receive, 'user_pw': pw_hash})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.post("/api/register")
def register_api():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "user_id": username_receive,
        "user_pw": password_hash,
        "user_img": 'default.png',
        "user_nick": username_receive
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.post("/api/register/check_dup")
def register_check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"user_id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.post("/api/user/update/img")
def user_update_img():
    # 이미지 파일(아바타) & 유저ID 가져오기
    file = request.files['user_img']
    user_id = request.form['user_id']

    # 파일 이름 & 파일 위치 문자열 만들기
    # file_name: 확장자 없는 파일 이름.
    # file_fullname: 확장자 있는 파일 이름.
    # file_dir: 파일 위치
    file_name = f'avatar_{user_id}'
    file_fullname = file_name + f'.{file.filename.split(".")[1]}'
    file_dir = 'static/images/avatars/'
    save_to = file_dir + file_fullname

    # 아바타가 저장되는 폴더에 동일한 이름의 파일이 있는 지 검색. 있으면 지우기.
    for prev_file in os.listdir(file_dir):
        if prev_file.startswith(file_name):
            os.remove(file_dir + prev_file)

    # local에 이미지파일로 저장 후, DB에 update
    file.save(save_to)
    db.users.update_one({'user_id': user_id}, {'$set': {'user_img': file_fullname}})

    return jsonify({'msg': '수정되었습니다.'})


@app.post("/api/user/update/nick")
def user_update_nick():
    user_id = request.form['user_id']
    user_nick = request.form['user_nick']

    db.users.update_one({'user_id': user_id}, {'$set': {'user_nick': user_nick}})

    return jsonify({'msg': '수정되었습니다'})


# @app.post("/api/user/delete")
# def user_delete():
#     return jsonify({'msg': "ok!!"})


@app.post("/api/review/create")
def review_create():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    star = request.form['star_give']
    desc = request.form['desc_give']
    user = payload['id']
    movie = request.form['id_give']

    doc = {
        'review_star': int(star),
        'review_desc': desc,
        'review_movie': movie,
        'review_user': user
    }

    db.reviews.insert_one(doc)
    return jsonify({'msg': '등록이 완료되었습니다!'})


@app.post("/api/review/update")
def review_update():
    # data 가져오기
    user_id = request.form['user_id']
    movie_id = request.form['movie_id']
    review_desc = request.form['review_desc']
    review_star = request.form['review_star']

    # movie_id와 user_id로 작성한 리뷰 찾아 update
    db.reviews.update_one(
        {"$and": [{"review_user": user_id}, {"review_movie": movie_id}]},
        {
            '$set': {
                'review_desc': review_desc, 'review_star': review_star
            }
        }
    )

    return jsonify({'msg': '수정되었습니다!!'})


@app.post("/api/review/delete")
def review_delete():
    user_id = request.form['user_id']
    movie_id = request.form['movie_id']

    db.reviews.delete_one(
        {"$and": [{"review_user": user_id}, {"review_movie": movie_id}]}
    )

    return jsonify({'msg': '삭제되었습니다!!'})


##################################################
# Run
##################################################


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)