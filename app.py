from bson import ObjectId
from flask import Flask, make_response, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, decode_token
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
   #  resp = make_response()
   #  resp.set_cookie('token',access_token)
    return jsonify({'result':'success','token':access_token})

#사용자 권환 확인 api
@app.route("/authChk",methods=['POST'])
def authChk():
    token = request.json.get('token')
    print("token:",token)
    if not token:
        return jsonify({'msg':'Token is missing'}), 400
    
    try:
        decoded_token = decode_token(token)
        identity = decoded_token['sub']
        authority=db.users.find_one({'id':identity},{'_id':0,'id':0,'password':0,'name':0})
        print("autaut",authority)
        print("authauth",authority['admin'])
        if authority['admin'] == True :
            return render_template('')
        return jsonify(logged_in_as=identity),200
    except Exception as e:
        return jsonify({"msg":"Invalid token"}), 400
    

# def check_access_token(access_token):
#     token = request.
#     try:
#         payload = jwt.decode()

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwagrs):
#         access_token = request.headers.get('Authorization')
#         if access_token is not None:
#             payload = check_access_token(access_token) #토큰의 유효성 확인


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
    user_list=list(db.users.find({},{'_id':0,'id':0,'password':0,'admin':0}))
    print("이게뭐람",user_list)
   #  return jsonify({'data':user_list})
    return jsonify({'result':'success','data':user_list})


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
    db.users.insert_one({'id':reg_id,'password':reg_pwd,'name':reg_name, 'admin':False})
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
    db.messages.insert_one({'id': u_id, 'message': msg, 'stat_appr': 'Ignore', 'stat_read': False, 'date':now_date})
    # 수신자와 질문내용 그리고 처리되지 않았다는 의미의 플래그를 질문 테이블에 저장
    return jsonify({"result":"success"})

#받은 메시지 출력 api
@app.route("/inbox", methods=["POST","GET"])
def recevedMsg():
    token = request.cookies.get('token')
   #  token = request.json.get('token')
    print("token:",token)
    if not token:
        return jsonify({'msg':'Token is missing'}), 400
    
    try:
        decoded_token = decode_token(token)
        u_id = decoded_token['sub']
        messages=objectIdDecoder(list(db.messages.find({'id':u_id})))
        print('message:',messages)
      #   return jsonify({'redirect':'/inboxRedirect'})
        return render_template('inbox.html',messagelist=messages)

    except Exception as e:
        return jsonify({"msg":"Invalid token"}), 400
   #디비연동코드
   #메시지 변수에 해당 아이디가 가지고 있는 정보 전부전달

   #질문테이블에서 본인 아이디의 받은 메시지를 select

# objectId제거 함수
def objectIdDecoder(list):
  results=[]
  for document in list:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results    

#받은 메시지 관리자 api
@app.route("/adminMsg", methods=["POST","GET"])
def adminMsg() :
   #디비연동코드
   #질문테이블에서 모든 메시지를 select
    messages=list(db.messages.find({'_id':False}))
    print("message:",messages)
    return render_template('adminhome.html',userMessageList=messages)
 
#메시지 읽음처리 api
@app.route('/receive/msgRead', methods=["POST"])
def msgRead():
    print(request.json)
    msg_id = request.json['msg_id']

    if msg_id is None:
        return jsonify({"error": "msg_id and status are required"}), 400

    try:
        object_id = ObjectId(msg_id)
    except Exception as e:
        return jsonify({"error": "Invalid msg_id format"}), 400
    
    #해당 메시지의 상태값 수정
    db.messages.update_one({'_id':object_id},{'$set':{'stat_read':True }})
    return jsonify({'result':'success'})

#메시지 승인/거절 api
@app.route('/adminMsg/check', methods=['POST'])
def msgCheck():
    print(request.json)
    msg_id     = request.json['m_id']
    status     = request.json['stat_appr']
   #  msg_id     = "6684b711db12e679fd9d8651"
   #  status     = "ignore"
   #  msg_id=getObjectId(msg_id)

    if msg_id is None or status is None:
        return jsonify({"error": "msg_id and status are required"}), 400

    try:
        object_id = ObjectId(msg_id)
    except Exception as e:
        return jsonify({"error": "Invalid msg_id format"}), 400

    print('objectId:', object_id)

   #  object_id=ObjectId(msg_id)
   #  print('objectId:',object_id)
   
    db.messages.update_one({'_id':object_id},{'$set':{'stat_appr':status }})
    print(db.messages.find_one({'_id':object_id}))
    #디비 연동 코드
    #디비에 해당 메시지 상태 업데이트
    
    return jsonify({'result':'success'})

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
    name_list = [
        {
            'name': '건우',
            'id': 1
        },
        {
            'name': '형욱',
            'id': 2
        }
    ]
    return render_template('home.html', title='또치에게 상대방 이름을 말해주세요', name_list=name_list)

@app.route('/question')
def question():
    return render_template('question.html', title='질문할 내용을 알려주세요')

@app.route('/testet')
def test():
    return render_template('test.html')

#리다이렉션 테스트 용으로 사용중
@app.route('/inboxRedirect')
def inboxRedirect():
    return render_template('inbox.html',)

#리다이렉션 Cookie 테스트 용으로 사용중
@app.route('/cookie')
def inboxCookie():
    token = request.cookies.get('token')
    decoded_token = decode_token(token)
    u_id = decoded_token['sub']
    messages=objectIdDecoder(list(db.messages.find({'id':u_id})))
    print('message:',messages)
    
    return render_template('inbox.html',messagelist=messages)





@app.route('/inboxdd')
def inbox():
    # messagelist = [
    #     {
    #         id: 1,
    #         content: '안녕하세요, 첫 번째 편지입니다.',
    #         userRead: false,
    #         admin: false,
    #     },
    #     {
    #         id: 2,
    #         content: '두 번째 편지입니다. 새로운 소식이 있습니다.',
    #         userRead: true,
    #         admin: false,
    #     },
    #     {
    #         id: 3,
    #         content: '관리자가 보낸 중요한 알림입니다.',
    #         userRead: false,
    #         admin: true,
    #     },
    #     {
    #         id: 4,
    #         content: '네 번째 편지입니다. 오늘 날씨가 참 좋네요.',
    #         userRead: true,
    #         admin: false,
    #     },
    #     {
    #         id: 5,
    #         content: '다섯 번째 편지입니다. 주말 잘 보내세요.',
    #         userRead: false,
    #         admin: false,
    #     },
    # ],
    return render_template('inbox.html')

@app.route('/chat')
def chatpage():
    return render_template('chat.html')

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@app.route('/test2')
def test2():
    return render_template('test2.html')

def testFunc():
   #  db.users.insert_one({'id':'test2','password':'qwer','name':'test','admin':'False'})
    db.message.insert_one({'id':'test1','message':'hi hello nihao','stat_appr':'False','stat_read':'False','date':'2024-07-02'})
    db.message.insert_one({'id':'test2','message':'hi hello nihao','stat_appr':'False','stat_read':'False','date':'2024-07-02'})

    all_users = list(db.users.find({}))
    print(all_users)
    return jsonify({'result':'success'})


if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)
