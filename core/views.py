from django.shortcuts import render
from django.http import Http404
from .utils import paginate

def index(request):
    questions = []
    for i in range(1, 80):
        questions.append({
            'id': i,
            'title': f'Question #{i}',
            'text': 'Some preview text for question...',
        })

    page = paginate(questions, request, per_page=20)
    return render(request, "index.html", {"page": page})


def hot(request):
    hot_questions = []
    for i in range(1, 60):
        hot_questions.append({
            'id': i,
            'title': f'Hot Question #{i}',
            'text': 'Hot question text...',
        })

    page = paginate(hot_questions, request, per_page=20)
    return render(request, "index.html", {"page": page})


def tag(request, tag):
    questions = []
    for i in range(1, 50):
        questions.append({
            'id': i,
            'title': f'Question tagged with {tag} #{i}',
            'text': f'This question has tag {tag}.',
        })

    page = paginate(questions, request, per_page=20)
    return render(request, "tag.html", {"page": page, "tag": tag})


def question(request, qid):
    if qid < 1 or qid > 200:
        raise Http404

    question = {
        "id": qid,
        "title": f"Question #{qid}",
        "text": "This is detailed question text, visible on question page."
    }

    # ответы (рыба)
    answers = []
    for i in range(1, 65):
        answers.append({
            "text": f"Answer #{i} to question {qid}",
            "score": i % 7,
        })

    page = paginate(answers, request, per_page=30)

    return render(request, "question.html", {
        "question": question,
        "page": page
    })


def login_view(request):
    return render(request, "login.html")


def signup_view(request):
    return render(request, "signup.html")


def ask(request):
    return render(request, "ask.html")
