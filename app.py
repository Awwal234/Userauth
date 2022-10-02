from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5683ebhty098'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/brim_app')
def brim_app():
    return render_template('brim.html')


@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('brim_app'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    # user = User.query.filter_by(email=email).first()
    # if user:
    #     return redirect(url_for('login'))

    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)
