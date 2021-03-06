from django.urls import path

from . import views
from .views import jsonresponse

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('question_form/', views.newquestion, name='newquestion'),
    path('create-question/', views.createquestion, name='createquestion'),
    path('api/', jsonresponse.as_view(), name='jsonresponse'),
]