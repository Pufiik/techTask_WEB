from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Question, Answer, Tag, best_users

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}',
        'tags': ['VK']
    } for i in range(10)
]

ANSWERS = [
    {
        'body': f'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in sapien ultricies justo convallis lacinia ac a ex. Praesent euismod pellentesque odio eu sodales. Curabitur pulvinar enim eu laoreet ullamcorper. Suspendisse viverra diam pellentesque lectus tincidunt, et sagittis arcu iaculis. Suspendisse potenti. Phasellus eu venenatis felis, dictum vulputate tortor. Cras lectus ipsum, faucibus et ultricies quis, feugiat non diam. Vivamus semper quis lectus ut congue. Nunc venenatis dui in tortor sodales, a scelerisque erat gravida. Nulla eleifend iaculis dui a scelerisque. Phasellus eleifend leo urna. Fusce ut facilisis urna. Donec egestas enim eu odio ultrices aliquet. {i * i}',
    } for i in range(3)
]

for q in QUESTIONS:
    if q['id'] % 2 == 0:
        q['tags'].append('TechnoPark')
    else:
        q['tags'].append('Kotlin')


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
    return render(request, 'main.html', {'questions': paginate(Question.question_items.new(), page), 'users': best_users(5), 'tags': Tag.objects.all()})


def login(request):
    return render(request, 'login.html', {'users': best_users(5), 'tags': Tag.objects.all()})


def reg(request):
        return render(request, 'reg.html', {'users': best_users(5), 'tags': Tag.objects.all()})


def settings(request):
    return render(request, 'settings.html', {'users': best_users(5), 'tags': Tag.objects.all()})


def ask(request):
    return render(request, 'ask.html', {'users': best_users(5), 'tags': Tag.objects.all()})


def single(request, question_id):
    return render(request, 'single.html', {'question': Question.question_items.single(q_id=question_id), 'answers': Answer.answer_items.get_answers(question_id), 'users': best_users(5), 'tags': Tag.objects.all()})


def tags(request, tag_name):
    page = request.GET.get('page', 1)
    return render(request, 'tags.html',
                  {'questions': paginate(Question.question_items.filter_by_tag(tag_name=tag_name), page),
                   'tag_name': tag_name, 'users': best_users(5), 'tags': Tag.objects.all()}, )


def hot(request, num=3):
    page = request.GET.get('page', 1)
    return render(request, 'hot.html', {'questions': paginate(Question.question_items.best(n=num), page), 'num': num, 'users': best_users(5), 'tags': Tag.objects.all()})
