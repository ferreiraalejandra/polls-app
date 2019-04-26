from rest_framework import serializers
from .models import Question, Choice

class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()
    username = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

   
class ChoiceSerializer(serializers.Serializer):
    choice_text = serializers.CharField(max_length=200)
    votes = serializers.IntegerField(default=0)