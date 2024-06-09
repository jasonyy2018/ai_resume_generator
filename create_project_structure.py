import os

# 定义要创建的项目结构
project_structure = {
    "ai_resume_generator": [
        "manage.py",
        "myproject/__init__.py",
        "myproject/asgi.py",
        "myproject/settings.py",
        "myproject/urls.py",
        "myproject/wsgi.py",
        "resume/__init__.py",
        "resume/admin.py",
        "resume/apps.py",
        "resume/models.py",
        "resume/tests.py",
        "resume/urls.py",
        "resume/views.py",
        "resume/templates/index.html",
        "resume/templates/generate_resume.html",
        "resume/templates/signup.html",
        "resume/templates/login.html",
        "resume/migrations/__init__.py",
        "resume/utils.py"
    ]
}

# 创建目录和文件
for root, files in project_structure.items():
    for file in files:
        file_path = os.path.join(root, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            pass

print("项目结构创建完成！")