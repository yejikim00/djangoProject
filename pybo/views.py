from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    page = request.GET.get('page', '1') # 페이지, GET 방식으로 호출된 URL에서 page 값을 가져올 때 사용. (pybo/?page=1) 만약 (pybo/)처럼 page 값이 없으면 디폴트 1.
    """
    pybo 목록 출력
    """ # Question.objects.order_by: 질문 목록 데이터, order_by: 조회 결과 정렬하는 함수. -: 역순으로 정렬해라(작성일시 역순으로 정렬). 최신순으로 보니까!
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기, question_list: 게시물 전체. 10: 페이지당 보여줄 게시물의 개수
    page_obj = paginator.get_page(page)   # 요청된 페이지에 해당하는 페이징 객체 생성. 해당 페이지의 데이터만 조회하도록 쿼리가 변경됨.
    context = {'question_list': page_obj} # question_list는 페이징 객체(page_obj)를 의미.
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


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 게정 저장.
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':    # 데이터 입력이 끝나 '저장하기=submit'을 누르면 post요청으로 바뀜.
        form = QuestionForm(request.POST)   # form에 데이터 저장, request.POST: 사용자가 입력한 내용이 담김.
        if form.is_valid():
            question = form.save(commit=False)  # commit=False: 임시 저장
            question.author = request.user  # author 속성에 로그인 계정 저장.
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')   # 데이터 저장 후 다시 질문 목록 보여주기 위해 index 불러옴.
    else:   # 처음엔 url밖에 전해주지 않으니 무조건 GET요청. 데이터 담을 수 있는 form을 불러옴.
        form = QuestionForm()
    context = {'form': form}    # {'form': form}: 템플릿에서 질문 등록시 사용할 폼 엘리먼트 생성.
    return render(request, 'pybo/question_form.html', context)  # 이게 데이터 입력하는 form창 불러오는 것.


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)  # instance 값을 기준으로 QuestionForm을 생성하지만, request.POST 값으로 덮어써라.
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)  # 폼의 속성값이 instance 값으로 채워짐. 따라서 수정 화면에는 기존의 제목과 내용이 채워져 있음.
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)