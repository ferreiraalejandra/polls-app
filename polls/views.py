from django.utils import timezone
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from .forms import questionForm



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
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
    question = get_object_or_404(Question, pk=question_id)
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
    if request.method == 'POST':
        form = questionForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = questionForm()

    return render(request, 'polls/question_form.html', {'form': form})


def createquestion(request):
    print(request.POST)
    questionText = request.POST['new_question']
    createdQuestion = Question(question_text=questionText, pub_date=timezone.now())

    createdQuestion.save()
    
    choiceOne = request.POST['choice_one']
    createdQuestion.choice_set.create(choice_text=choiceOne, votes=0)
    
    choiceTwo = request.POST['choice_two']
    createdQuestion.choice_set.create(choice_text=choiceTwo, votes=0)

    choiceThree = request.POST['choice_three']
    createdQuestion.choice_set.create(choice_text=choiceThree, votes=0)

    return render(request, 'polls/saved_question.html')