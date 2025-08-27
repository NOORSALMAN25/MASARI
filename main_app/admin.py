from django.contrib import admin
from .models import Question , Answer , University, Program, Favorite

# Register your models here.
class AnswerInline(admin.TabularInline):   
    model = Answer
    extra = 1   

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(University)
admin.site.register(Program)
admin.site.register(Favorite)
