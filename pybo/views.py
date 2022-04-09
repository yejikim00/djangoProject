from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm


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


def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':    # 데이터 입력이 끝나 '저장하기=submit'을 누르면 post요청으로 바뀜.
        form = QuestionForm(request.POST)   # f답rm에 데이터 저장, request.POST: 사용자가 입력한 내용이 담김.
        if form.is_valid():
            question = form.save(commit=False)  # commit=False: 임시 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')   # 데이터 저장 후 다시 질문 목록 보여주기 위해 index 불러옴.
    else:   # 처음엔 url밖에 전해주지 않으니 무조건 GET요청. 데이터 담을 수 있는 form을 불러옴.
        form = QuestionForm()
    context = {'form': form}    # {'form': form}: 템플릿에서 질문 등록시 사용할 폼 엘리먼트 생성.
    return render(request, 'pybo/question_form.html', context)  # 이게 데이터 입력하는 form창 불러오는 것.