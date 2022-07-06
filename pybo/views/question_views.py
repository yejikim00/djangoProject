from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


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


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')