from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import datetime, timedelta
from pymongo import MongoClient

#pymongo 변수 선언
client = MongoClient('localhost',27017)
db = client.w00_jungdaejun

app = Flask(__name__)

admin_id = "hjo"
admin_pw = "12345"
SECRET_KEY="hyounguk"
app.config["JWT_SECRET_KEY"] = SECRET_KEY  # JWT토큰 키
jwt = JWTManager(app)

#로그인 api
@app.route("/loginJWT", methods=["POST"])
def login():
    username = request.json['id'] # request.form에서 아이디와 패스워드 파싱
    password = request.json['pwd']
    
    print(request)

    user_id = db.users.find_one({'id':username})
    if user_id == None:
        print("fail")
        return jsonify({"result":"false"}), 401
    
    if user_id['password'] != password :
        print("fail")
        return jsonify({"ressult":"false"}), 401
    

   #  if username != admin_id or password != admin_pw: # 만약 아이디와 비밀번호가 다를 시 에러 처리
   #      return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    print(access_token)
    return jsonify({'token':access_token})

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

#로그인 성공시 hompage창
@app.route("/test_home")
def testHome():
    user_list=list(db.users.find({}))
    print("이게뭐람",user_list)
   #  return jsonify({'data':user_list})
    return jsonify({'data':'success'})


#가입창 클릭시 가입화면전환
@app.route("/signup", methods=["POST"])
def register():
    return render_template('signup.html')

#가입화면에서 가입버튼 클릭 시 폼 전달
@app.route('/signup/api', methods=['POST'])
def api_register():
    
   #  print(request)
   #  # 전달받은 request form 파싱
    reg_id     = request.json['id'] 
    reg_pwd    = request.json['pwd']
    reg_name   = request.json['name']
    reg_admin  = False

   #비밀번호 암호화 코드 필요
   #  print(reg_id)   
   #디비연동
    db.users.insert_one({'id':reg_id,'password':reg_pwd,'name':reg_name, 'admin':"False"})
    find_one = db.users.find({'id':'test'})
    print(find_one)
   #아이디와 패스워드 이름을 가입자 테이블에 추가
    return jsonify({'result':'success'})

#질문 폼 api
@app.route("/question/send",methods=["POST"])
def questionSend():
    print("질문 폼 요청값:",request.json)
    #입력받은 폼 파싱
    u_id    = request.json['u_id']
    msg     = request.json['msg']

    now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 디비 연동
    db.messages.insert_one({'id': u_id, 'message': msg, 'stat_appr': False, 'stat_read': False, 'date':now_date})
    # 수신자와 질문내용 그리고 처리되지 않았다는 의미의 플래그를 질문 테이블에 저장
    return jsonify({"result":"success"})

#받은 메시지 출력 api
@app.route("/receive", methods=["GET"])
def recevedMsg():
    u_id = request.args.get("u_id")
   #디비연동코드
   #메시지 변수에 해당 아이디가 가지고 있는 정보 전부전달
    messages=list(db.messages.find({'id':u_id}))
   #질문테이블에서 본인 아이디의 받은 메시지를 select
    return jsonify({'result':'success','data':messages})

#받은 메시지 관리자 api
@app.route("/adminMsg", methods=["POST"])
def adminMsg() :
   #디비연동코드
   #질문테이블에서 모든 메시지를 select
    messages=list(db.messages.find())
    return jsonify({'result':'success','data':messages})
 
#메시지 읽음처리 api
@app.route('/receive/msgRead', methods=["POST"])
def msgRead():
    msg_id = request.json('msg_id')
    #해당 메시지의 상태값 수정
    db.message.update_one({'_id':msg_id},{'$set':{'stat_read':True }})
    return jsonify({'result':'success'})

#메시지 승인/거절 api
@app.route('/adminMsg/check', methods=['POST'])
def msgCheck():
    msg_id    = request.json['msg_id']
    status  = request.json['status']
    db.message.update_one({'_id':msg_id},{'$set':{'stat_appr':status }})

    #디비 연동 코드
    #디비에 해당 메시지 상태 업데이트
    
    return jsonify({'status':'success'})

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/homepage')
def home_page():
    return render_template('home.html')

@app.route('/question')
def question():
    return render_template('question.html')

@app.route('/inbox')
def inbox():
    return render_template('inbox.html')

@app.route('/chat')
def chatpage():
    return render_template('chat.html')

@app.route('/test')
def testFunc():
   #  db.users.insert_one({'id':'test2','password':'qwer','name':'test','admin':'False'})
    db.message.insert_one({'id':'test1','message':'hi hello nihao','stat_appr':'False','stat_read':'False','date':'2024-07-02'})
    db.message.insert_one({'id':'test2','message':'hi hello nihao','stat_appr':'False','stat_read':'False','date':'2024-07-02'})

    all_users = list(db.users.find({}))
    print(all_users)
    return jsonify({'result':'success'})


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)