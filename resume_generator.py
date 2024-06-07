def generate_resume(name, email, experience, education):
    resume_template = f"""
    姓名: {name}
    邮箱: {email}

    工作经历:
    {experience}

    教育背景:
    {education}
    """
    return resume_template