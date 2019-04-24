from rest_framework import serializers
from .models import Question, Choice

class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=200)
  
   
class ChoiceSerializer(serializers.Serializer):
    choice_text = serializers.CharField(max_length=200)
