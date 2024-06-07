from flask import Flask, request, render_template
from resume_generator import generate_resume

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_resume', methods=['POST'])
def generate_resume_route():
    name = request.form['name']
    email = request.form['email']
    experience = request.form['experience']
    education = request.form['education']

    resume_content = generate_resume(name, email, experience, education)
    return render_template('resume.html', resume_content=resume_content)

if __name__ == '__main__':
    app.run(debug=True)