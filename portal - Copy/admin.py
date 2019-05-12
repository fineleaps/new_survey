from django.contrib import admin
from .models import Question, Choice, Answer, Survey, MySession


class ChoiceInline(admin.TabularInline):

    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):

    model = Question
    extra = 1


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on')
    inlines = (QuestionInline, )


class QuestionAdmin(admin.ModelAdmin):
    list_display_links = ('display_link', )
    list_display = ('display_link', 'survey', 'question_text', 'serial_number')
    list_editable = ('question_text', 'survey', 'serial_number')
    inlines = (ChoiceInline, )

    list_filter = ('survey', )


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(MySession)
