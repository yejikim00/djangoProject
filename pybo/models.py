from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)  # CharField: 글자수 제한에 사용. max_length: 최대 글자수.
    content = models.TextField()  # TextField: 글자수 제한 없음.
    create_date = models.DateTimeField()  # DateTimeField: 날짜, 시간에 관계된 속성.
    modify_date = models.DateTimeField(null=True, blank=True)  # 값이 비어있어도 상관없다. 수정한 경우에만 생성되면 되기 떄문.

    def __str__(self):
        return self.subject


class Answer(models.Model):  # ForeignKey: 다른 모델을 속성으로 가지기 위해 사용. on_delete=models.CASCADE: 속성 모델이 삭제될 경우 현재 모델도 삭제.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
