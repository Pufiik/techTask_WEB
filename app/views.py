from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
        'body': f'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin in sapien ultricies justo convallis lacinia ac a ex. Praesent euismod pellentesque odio eu sodales. Curabitur pulvinar enim eu laoreet ullamcorper. Suspendisse viverra diam pellentesque lectus tincidunt, et sagittis arcu iaculis. Suspendisse potenti. Phasellus eu venenatis felis, dictum vulputate tortor. Cras lectus ipsum, faucibus et ultricies quis, feugiat non diam. Vivamus semper quis lectus ut congue. Nunc venenatis dui in tortor sodales, a scelerisque erat gravida. Nulla eleifend iaculis dui a scelerisque. Phasellus eleifend leo urna. Fusce ut facilisis urna. Donec egestas enim eu odio ultrices aliquet. {i*i}',
    } for i in range(3)
]

for q in QUESTIONS:
    if q['id'] % 2 == 0:
        q['tags'].append('TechnoPark')
    else:
        q['tags'].append('Kotlin')


def paginate(objects, page, page_count=3):
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
    return render(request, 'main.html', {'questions': paginate(QUESTIONS, page)})


def login(request):
    return render(request, 'login.html')


def reg(request):
    if request.method == 'POST':
        return render(request, 'login.html')
    else:
        return render(request, 'reg.html')


def settings(request):
    return render(request, 'settings.html')


def ask(request):
    return render(request, 'ask.html')


def single(request, question_id):
    question = QUESTIONS[question_id]
    return render(request, 'single.html', {'question': question, 'answers': ANSWERS})



def tags(request, tag_name):
    tag_question = []
    page = request.GET.get('page', 1)
    for item in QUESTIONS:
        if tag_name in item['tags']:
            tag_question.append(item)
    return render(request, 'tags.html', {'questions':  paginate(tag_question, page), 'tag_name': tag_name})

def hot(request):
    page = request.GET.get('page', 1)
    return render(request, 'hot.html', {'questions': paginate(QUESTIONS, page)})