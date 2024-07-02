from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/homepage')
def homepage():
    return render_template('home.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)