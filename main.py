from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# -------------------- DATABASE SETUP --------------------

class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# -------------------- FLASK-LOGIN SETUP --------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# -------------------- USER MODEL --------------------

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))


with app.app_context():
    db.create_all()

# -------------------- ROUTES --------------------

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        existing_user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()

        if existing_user:
            flash("You have already registered. Please log in.")
            return redirect(url_for("login"))

        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email=email,
            password=hashed_password,
            name=name
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('secrets'))

    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar()

        if not user:
            flash("This email does not exist. Please register first.")
            return redirect(url_for("login"))

        if not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for('secrets'))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


@app.route('/download')
@login_required
def download():
    return send_from_directory(
        directory="static/files",
        path="cheat_sheet.pdf",
        as_attachment=True
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)