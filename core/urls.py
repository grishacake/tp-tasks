from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("hot/", views.hot, name="hot"),
    path("tag/<str:tag>/", views.tag, name="tag"),
    path("question/<int:qid>/", views.question, name="question"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("ask/", views.ask, name="ask"),
]