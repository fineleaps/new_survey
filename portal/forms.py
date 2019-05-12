from django import forms
from .models import Answer, Survey, Choice, Question, Response
#
#
# class AnswerForm(forms.ModelForm):
#
#     choice = forms.ModelChoiceField()
#
#     def __init__(self, question, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if question:
#             self.fields['choice'].queryset = question.choice_set.all()
#
#     class Meta:
#         model = Answer
#         fields = ('question', 'choice')
