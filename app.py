from flask import session 
from flask_socketio import emit        
from bson import ObjectId
from flask import Flask, make_response, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, decode_token
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask_socketio import SocketIO
from flask_socketio import SocketIO, send

#pymongo 변수 선언
client = MongoClient('localhost',27017)
db = client.w00_jungdaejun

app = Flask(__name__)
socket_io = SocketIO(app)

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

    access_token = create_access_token(identity=username)
    print(access_token)
    return jsonify({'result':'success','token':access_token})

#사용자 권환 확인 api
@app.route("/authChk",methods=['POST','GET'])
def authChk():
    token = request.cookies.get('token')
    print("token:",token)
    if not token:
        return jsonify({'msg':'Token is missing'}), 400
    
    try:
        decoded_token = decode_token(token)
        identity = decoded_token['sub']
        print("identity",identity)
        authority=db.users.find_one({'id':identity},{'_id':0,'password':0,'name':0})
        print("autaut",authority)
        print("authauth",authority['admin'])
        if authority['admin'] == True :
            messages = list(db.messages.find({}))
            print(messages)
            return render_template('adminhome.html',userMessageList=messages)
        messages = list(db.users.find({}))
        print("messages:",messages)
        return render_template('home.html',name_list=messages)
    except Exception as e:
        print("error",e)
        return jsonify({"msg":"Invalid token"}), 400

#가입창 클릭시 가입화면전환
@app.route("/signup", methods=["POST"])
def register():
    return render_template('signup.html')

#가입화면에서 가입버튼 클릭 시 폼 전달
@app.route('/signup/api', methods=['POST'])
def api_register():
   #  # 전달받은 request form 파싱
    reg_id     = request.json['id'] 
    reg_pwd    = request.json['pwd']
    reg_name   = request.json['name']
    reg_admin  = False

   #비밀번호 암호화 코드 필요
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
    u_id    = request.json['id']
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
    print("test:",request.json)
    msg_id = request.json['m_id']

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
    m_id     = request.json['m_id']
    status     = request.json['stat_appr']

    if m_id is None or status is None:
        return jsonify({"error": "msg_id and status are required"}), 400
    try:
        object_id = ObjectId(m_id)

    except Exception as e:
        return jsonify({"error": "Invalid msg_id format"}), 400

    print('objectId:', object_id)
    db.messages.update_one({'_id':object_id},{'$set':{'stat_appr':status }})
    print(db.messages.find_one({'_id':object_id}))
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

@app.route('/question')
def question():
    return render_template('question.html', title='질문할 내용을 알려주세요')

#리다이렉션 테스트 용으로 사용중
@app.route('/inboxRedirect')
def inboxRedirect():
    return render_template('inbox.html')

#리다이렉션 테스트 용으로 사용중
@app.route('/test')
def test():
    return render_template('test.html')

#리다이렉션 Cookie 테스트 용으로 사용중
@app.route('/cookie')
def inboxCookie():
    token = request.cookies.get('token')
    decoded_token = decode_token(token)
    u_id = decoded_token['sub']
    messages=objectIdDecoder(list(db.messages.find({'id':u_id})))
    print('message:',messages)
    
    return render_template('inbox.html',messagelist=messages)

def socketio_init(socketio):
    @socketio.on('testSocket',namespace='/test')
    def testEvent(message):
        print('socketio',socketio)
        tsession = session.get('test')
        print('received message'+str(message))
        retMessage = { 'msg' : "hello response" }
        emit('test',retMessage,callback=tsession)

@app.route('/chat')
def chatting():    
    return render_template('chat.html')

@socket_io.on("message")
def handle_message(message):    
    print("message: " + message)    
    to_client = {}
    if message == 'new_connect':        
        to_client['message'] = "새로운 유저가 난입하였다!!"        
        to_client['type'] = 'connect'  
    else:        
        to_client['message'] = message        
        to_client['type'] = 'normal'    
        print('socket_io',socket_io)  
    send({'sender': request.sid, 'message': message}, broadcast=True)

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)