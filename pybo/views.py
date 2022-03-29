from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    """
    pybo 목록 출력
    """ # Question.objects.order_by: 질문 목록 데이터, order_by: 조회 결과 정렬하는 함수. -: 역순으로 정렬해라(작성일시 역순으로 정렬). 최신순으로 보니까!
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)
    # render함수: 파이썬 데이터를 템플릿에 적용해 html로 반환하는 함수. question_list 데이터를 thml 파일에 적용해 html을 리턴.
    # 템플릿 파일: 장고에서 사용하는 태그를 사용할 수 있는 html 파일.


def detail(request, question_id):
    """
    pybo 내용 츌력
    """
    question = get_object_or_404(Question, pk=question_id) # pk: Question 모델의 기본키(Primary Key)=id
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
