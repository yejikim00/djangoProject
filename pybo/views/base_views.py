from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question


def index(request):
    page = request.GET.get('page', '1')  # 페이지, GET 방식으로 호출된 URL에서 page 값을 가져올 때 사용. (pybo/?page=1) 만약 (pybo/)처럼 page 값이 없으면 디폴트 1.
    """
    pybo 목록 출력
    """  # Question.objects.order_by: 질문 목록 데이터, order_by: 조회 결과 정렬하는 함수. -: 역순으로 정렬해라(작성일시 역순으로 정렬). 최신순으로 보니까!
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기, question_list: 게시물 전체. 10: 페이지당 보여줄 게시물의 개수
    page_obj = paginator.get_page(page)  # 요청된 페이지에 해당하는 페이징 객체 생성. 해당 페이지의 데이터만 조회하도록 쿼리가 변경됨.
    context = {'question_list': page_obj}  # question_list는 페이징 객체(page_obj)를 의미.
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