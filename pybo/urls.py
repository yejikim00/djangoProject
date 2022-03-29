from django.urls import path
from . import views


app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'), # index: http://localhost:8000/pybo/
    path('<int:question_id>/', views.detail, name='detail'), # int: 숫자가 매핑됨을 의미, detail: http://localhost:8000/pybo/2
]