from django.urls import path
from . import views


app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'), # index: http://localhost:8000/pybo/
    path('<int:question_id>/', views.detail, name='detail'), # int: 숫자가 매핑됨을 의미, detail: http://localhost:8000/pybo/2
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
]