from django import forms
from .models import Question, Choice


class questionForm(forms.Form):
    new_question= forms.CharField(label='New Question', max_length=300)
    choice_one= forms.CharField(label='Choice 1', max_length=100)
    choice_two= forms.CharField(label='Choice 2', max_length=100)
    choice_three= forms.CharField(label='Choice 3', max_length=100)
