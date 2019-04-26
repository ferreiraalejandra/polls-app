from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.views import APIView
from rest_framework import status

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Question, Choice
from django.urls import reverse
from .forms import questionForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
    
def vote(request, question_id):
    print(request.user.username)
    question = get_object_or_404(Question, pk=question_id)
    if request.user.username == question.username:
        return render(request, 'polls/error_response.html', {'question': question})
    else:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def newquestion(request):
    form = questionForm()
    return render(request, 'polls/question_form.html', {'form': form})



def createquestion(request):
    questionText = request.POST['new_question']
    choiceOne = request.POST['choice_one']
    choiceTwo = request.POST['choice_two']
    choiceThree = request.POST['choice_three']
    username = request.user.username

    createdQuestion = Question(question_text=questionText, pub_date=timezone.now(), username=username)
    createdQuestion.save()
    
    createdQuestion.choice_set.create(choice_text=choiceOne, votes=0)
    createdQuestion.choice_set.create(choice_text=choiceTwo, votes=0)
    createdQuestion.choice_set.create(choice_text=choiceThree, votes=0)

    return render(request, 'polls/saved_question.html')



class JSONResponse(APIView):
    def get(self, request):
        pollsQuestion = Question.objects.all()
        # pollsChoices = Choice.objects.all()

        # pollsElements = [
        #     {
        #         'pollsQuestion': pollsQuestion, 'pollsChoices': pollsQuestion, 
        #     },
        # ]
        # import pdb
        # pdb.set_trace()
        serializer =  QuestionSerializer(pollsQuestion, many=True)
        print(serializer.data)
        return Response({"questions": serializer.data})

    def post(self, request):
        questionText = request.data.get('new_question')
        # choiceOne = request.data.get('choice_one')
        # choiceTwo = request.data.get('choice_two')
        # choiceThree = request.data.get('choice_three')
        # username = request.data.get('username')

        # createdQuestion = Question(question_text=questionText, pub_date=timezone.now(), username=username)
        # createdQuestion.save()
        
        # createdQuestion.choice_set.create(choice_text=choiceOne, votes=0)
        # createdQuestion.choice_set.create(choice_text=choiceTwo, votes=0)
        # createdQuestion.choice_set.create(choice_text=choiceThree, votes=0)

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"Success": "Question was created successfully"})