from django.contrib import admin
from .models import User, Question, Answer, Tag, QuestionLike, AnswerLike

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'rating', 'created_at')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'rating', 'created_at')


admin.site.register(Tag)
admin.site.register(QuestionLike)
admin.site.register(AnswerLike)
