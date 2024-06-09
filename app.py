from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # 需要设置一个密钥用于会话

# 模拟的用户数据
users = {
    "admin": "password123"
}

# 默认模板设置
template_settings = {
    "title": "Resume",
    "heading_style": "Heading2",
    "body_style": "BodyText"
}

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html', template=template_settings)

@app.route('/set_template', methods=['POST'])
def set_template():
    if 'username' not in session:
        return redirect(url_for('login'))
    template_settings['title'] = request.form['title']
    template_settings['heading_style'] = request.form['heading_style']
    template_settings['body_style'] = request.form['body_style']
    return redirect(url_for('admin'))

# 其他处理简历生成的代码
@app.route('/generate_resume', methods=['POST'])
def generate_resume_route():
    # 假设定义了简历生成的代码
    pass

if __name__ == '__main__':
    app.run(debug=True)