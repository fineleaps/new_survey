from django import forms
from .models import Answer, Survey, Choice, Question

#
# class AnswerForm(forms.ModelForm):
#
#     choice = forms.ChoiceField(widget=forms.CheckboxInput(), choices=)
#
#     class Meta:
#         model = Answer
#         fields = ('choice', )