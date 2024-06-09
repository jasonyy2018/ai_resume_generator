import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from config import save_config, load_config
from flask_migrate import Migrate

app = Flask(__name__)

# Load configuration
config_data = load_config()

# Initialize the app configurations
app.secret_key = config_data.get('secret_key', 'super-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = config_data.get('database_uri', 'sqlite:///site.db')

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if config_data.get('configured'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_email = request.form['admin_email']
        admin_password = request.form['admin_password']
        host = request.form['host']
        port = request.form['port']
        database = request.form['database']
        user = request.form['user']
        password = request.form['password']
        secret_key = request.form['secret_key']

        database_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

        config_data['secret_key'] = secret_key
        config_data['database_uri'] = database_uri
        config_data['configured'] = True
        save_config(config_data)

        app.secret_key = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        db.create_all()

        new_user = User(username=admin_username, email=admin_email, password=admin_password, role='admin')
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('setup.html', config=config_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f'Hello, {session["username"]}!'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    if not config_data.get('configured'):
        app.run(debug=True)
    else:
        db.create_all()
        app.run(debug=True)