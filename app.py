from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from config import save_config, config
from db import db
from models import User

app = Flask(__name__)

if config:
    app.secret_key = config['secret_key']
    app.config['SQLALCHEMY_DATABASE_URI'] = config['database_uri']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if config:
        return redirect(url_for('login'))

    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_email = request.form['admin_email']
        admin_password = generate_password_hash(request.form['admin_password'])
        database_uri = request.form['database_uri']
        secret_key = request.form['secret_key']

        new_config = {
            "secret_key": secret_key,
            "database_uri": database_uri
        }
        save_config(new_config)

        app.secret_key = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        with app.app_context():
            db.create_all()
            new_user = User(username=admin_username, email=admin_email, password=admin_password, role='admin')
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('login'))

    return render_template('setup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/admin')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')


@app.route('/set_template', methods=['POST'])
def set_template():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    # 模板设置的逻辑可以在这里实现
    return redirect(url_for('admin'))


@app.route('/generate_resume', methods=['POST'])
def generate_resume_route():
    pass


if __name__ == '__main__':
    if not config:
        app.run(debug=True)  # 无配置，开放设置页面
    else:
        with app.app_context():
            db.create_all()  # 确保存在应用上下文
        app.run(debug=True)