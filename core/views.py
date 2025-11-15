from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .utils import paginate
from core.models import Question, Answer, Tag

def index(request):
    questions = Question.objects.new()
    page = paginate(questions, request, per_page=20)
    return render(request, "index.html", {"page": page})


def hot(request):
    questions = Question.objects.hot()
    page = paginate(questions, request, per_page=20)
    return render(request, "index.html", {"page": page})


def tag(request, tag):
    tag_obj = get_object_or_404(Tag, name=tag)
    questions = tag_obj.question_set.all().order_by('-rating')
    page = paginate(questions, request, per_page=20)
    return render(request, "tag.html", {"page": page, "tag": tag_obj})


def question(request, qid):
    q = get_object_or_404(Question, pk=qid)
    answers = Answer.objects.filter(question=q).order_by('-rating', '-created_at')
    page = paginate(answers, request, per_page=30)
    return render(request, "question.html", {"question": q, "page": page})

def login_view(request):
    return render(request, "login.html")


def signup_view(request):
    return render(request, "signup.html")


def ask(request):
    return render(request, "ask.html")
