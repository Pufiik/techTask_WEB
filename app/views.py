from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Answer, Tag, best_users


def paginate(objects, page, page_count=2):
    paginator = Paginator(objects, page_count)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return questions


def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'main.html', {'questions': paginate(Question.question_items.new(), page), 'users': best_users(5), 'tags': Tag.tag_items.popular_tags(6)})


def login(request):
    return render(request, 'login.html', {'users': best_users(5), 'tags': Tag.tag_items.popular_tags(6)})


def reg(request):
        return render(request, 'reg.html', {'users': best_users(5), 'tags': Tag.tag_items.popular_tags(6)})


def settings(request):
    return render(request, 'settings.html', {'users': best_users(5), 'tags': Tag.tag_items.popular_tags(6)})


def ask(request):
    return render(request, 'ask.html', {'users': best_users(6), 'tags': Tag.tag_items.popular_tags(5)})


def single(request, question_id):
    return render(request, 'single.html', {'question': Question.question_items.single(q_id=question_id), 'answers': Answer.answer_items.get_answers(question_id), 'users': best_users(5), 'tags':Tag.tag_items.popular_tags(6)})


def tags(request, tag_name):
    page = request.GET.get('page', 1)
    return render(request, 'tags.html',
                  {'questions': paginate(Question.question_items.filter_by_tag(tag_name=tag_name), page),
                   'tag_name': tag_name, 'users': best_users(5), 'tags': Tag.tag_items.popular_tags(6)}, )


def hot(request):
    page = request.GET.get('page', 1)
    return render(request, 'hot.html', {'questions': paginate(Question.question_items.best(), page), 'users': best_users(5), 'tags': Tag.tag_items.popular_tags(6)})
