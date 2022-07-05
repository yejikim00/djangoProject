from django.urls import path
from . import views


app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'), # index: http://localhost:8000/pybo/
    path('<int:question_id>/', views.detail, name='detail'), # int: 숫자가 매핑됨을 의미, detail: http://localhost:8000/pybo/2
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
]