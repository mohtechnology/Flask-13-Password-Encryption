from flask import Flask, render_template, redirect, session , request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(50), primary_key = True)
    password = db.Column(db.String(50), nullable = False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user' in session:
        return "Welcome to the home page"
    else:
        return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = True
            return redirect('/')
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(
            username = username,
            password = hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)