from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import datetime, timedelta
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
    return render_template('register.html')

#가입화면에서 가입버튼 클릭 시 폼 전달
@app.route('/api/register', methods=['POST'])
def api_register():
    # 전달받은 request form 파싱
    reg_id     = request.form['id'] 
    reg_pwd    = request.form['pwd']
    reg_email  = request.form['email']

   #비밀번호 암호화 코드 필요
      
   #디비연동

    return jsonify({'result':'success'})

@app.route("/question",methods=["POST"])
def question():
    #입력받은 폼 파싱
    s_id    = request.form['s_id']
    msg     = request.form['msg']
    # 디비 연동

    return jsonify({"result":"success"})



@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)