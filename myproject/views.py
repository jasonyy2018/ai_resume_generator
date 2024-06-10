from django.shortcuts import render
from .models import Resume


def index(request):
    return render(request, 'index.html')


def resume_generator(request):
    if request.method == 'POST':
        # 从表单获取数据并生成简历
        name = request.POST.get('name')
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')

        resume = Resume(name=name, education=education, experience=experience, skills=skills)
        resume.save()

        context = {'resume': resume}
        return render(request, 'resume.html', context)

    return render(request, 'resume.html')