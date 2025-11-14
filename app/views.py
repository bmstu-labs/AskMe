from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from typing import List

from .models import Question, Tag

ANSWERS = []


def paginate(request, objects, per_page=5):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def question(request, question_id: int):
    question = get_object_or_404(Question, pk=question_id)
        
    answers_page = paginate(request, ANSWERS)
    
    return render(
        request=request,
        template_name='question.html',
        context={
            'tags': get_top_n_tags(),
            'question': question,
            'answers': answers_page.object_list,
            'page_obj': answers_page
        }
    )


def questions(request):
    questions = Question.objects.all()
    questions_page = paginate(request, questions)

    return render(
        request=request,
        template_name='questions.html',
        context={
            'tags': get_top_n_tags(),
            'questions': questions_page.object_list,
            'page_obj': questions_page
        }
    )


def hot(request):
    questions = Question.objects.all()
    questions_page = paginate(request, questions)

    return render(
        request=request,
        template_name='hot.html',
        context={
            'tags': get_top_n_tags(),
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
        request=request,
        template_name='ask.html'
    )


def get_top_n_tags(n: int = 5) -> List[Tag]:
    tags = Tag.objects.all()
    return tags[:n]


def tag(request, tag: str):
    tag_obj = get_object_or_404(Tag, name=tag)

    questions = Question.objects.filter(tags=tag_obj).order_by('-created_at')

    questions_page = paginate(request, questions)

    return render(
        request=request,
        template_name='tag.html',
        context={
            'tags': get_top_n_tags(),
            'tag_name': tag_obj.name,
            'questions': questions_page.object_list,
            'page_obj': questions_page
        }
    )