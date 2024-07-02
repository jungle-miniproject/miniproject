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
    input_data=request.form
    username = input_data['id']
    password = input_data['pw']
    if username != admin_id or password != admin_pw:
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

@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5001,debug=True)