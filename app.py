from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import datetime, timedelta
from pymongo import MongoClient

#pymongo 변수 선언
client = MongoClient('localhost',27017)
db = client.jungle

from flask import Flask, render_template
app = Flask(__name__)

admin_id = "hjo"
admin_pw = "12345"
SECRET_KEY="hyounguk"
app.config["JWT_SECRET_KEY"] = SECRET_KEY  # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/loginJWT", methods=["POST"])
def login():
    username = request.form['id'] # request.form에서 아이디와 패스워드 파싱
    password = request.form['pwd']
    if username != admin_id or password != admin_pw: # 만약 아이디와 비밀번호가 다를 시 에러 처리
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    print(access_token)
    return jsonify({'reusult':'success','token':access_token})

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

#가입창 클릭시 가입화면전환
@app.route("/register", methods=["POST"])
def register():
    return render_template('signup.html')

#가입화면에서 가입버튼 클릭 시 폼 전달
@app.route('/api/signup', methods=['POST'])
def api_register():
    # 전달받은 request form 파싱
    reg_id     = request.form['id'] 
    reg_pwd    = request.form['pwd']
    reg_email  = request.form['email']

   #비밀번호 암호화 코드 필요
      
   #디비연동
   #아이디와 패스워드 이름을 가입자 테이블에 추가
    return jsonify({'result':'success'})

#질문 폼 api
@app.route("/question",methods=["POST"])
def question():
    #입력받은 폼 파싱
    u_id    = request.form['s_id']
    msg     = request.form['msg']
    # 디비 연동
    # 수신자와 질문내용 그리고 처리되지 않았다는 의미의 플래그를 질문 테이블에 저장
    return jsonify({"result":"success"})

#받은 메시지 출력 api
@app.route("/receive", methods=["GET"])
def recevedMsg():
    u_id = request.args.get("u_id")

   #디비연동코드
   #질문테이블에서 본인 아이디의 받은 메시지를 select
    return jsonify({'result':'success','data':data})

#받은 메시지 관리자 api
@app.route("/adminMsg", methods=["POST"])
def adminMsg() :
   #디비연동코드
   #질문테이블에서 모든 메시지를 select
    return jsonify({'result':'success','data':data})
 
#메시지 읽음처리 api
@app.route('/receive/msgRead', methods=["POST"])
def msgRead():
    
    return jsonify({'result':'success'})

#메시지 승인 거절 api
@app.route('/adminMsg/check', methods=['POST'])
def msgCheck():
    m_id    = request.form['m_id']
    status  = request.form['status']

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
def question_page():
    return render_template('question.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)