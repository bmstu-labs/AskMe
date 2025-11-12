from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404

QUESTIONS = [
    {
        'id': i,
        'title': f'Title #{i}',
        'text': 'Random text'
    } 
    for i in range(1, 31)
]

ANSWERS = [
    {
        'id': i + 1,
        'username': f'User #{i + 1}',
        'text': 'Answer Text',
    } 
    for i in range(30)
]


def paginate(request, objects, per_page = 5):
    page_number = int(request.GET.get('page', 1))
    
    paginator = Paginator(objects, per_page)
    page = paginator.page(page_number)

    return page


def question(request, question_id: int):
    question = next((q for q in QUESTIONS if q['id'] == question_id), None)
    if question is None:
        raise Http404()
        
    answers_page = paginate(request, ANSWERS)
    
    return render(
        request=request,
        template_name='question.html',
        context={
            'question': question,
            'answers': answers_page.object_list,
            'page_obj': answers_page
        }
    )


def questions(request):
    questions_page = paginate(request, QUESTIONS)

    return render(
        request=request,
        template_name='questions.html',
        context={
            'questions': questions_page.object_list,
            'page_obj': questions_page
        }
    )


def hot(request):
    questions_page = paginate(request, QUESTIONS[:5][::-1])

    return render(
        request=request,
        template_name='hot.html',
        context={
            'questions': questions_page.object_list,
            'page_obj': questions_page
        }
    )


def register(request):
    return render(
        request=request,
        template_name='register.html'
    )


def login(request):
    return render(
        request=request,
        template_name='login.html'
    )


def settings(request):
    return render(
        request=request,
        template_name='settings.html'
    )


def ask(request):
    return render(
        request=ask,
        template_name='ask.html'
    )