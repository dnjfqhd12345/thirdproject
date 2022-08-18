from django.db import models
from account.models import User
from django.urls import reverse
from account.models import Profile

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    has_comment = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wyw:index', args=[self.name])
    


class Posting(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    author_avatar = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='author_question')
    modify_date = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    voter = models.ManyToManyField(User, related_name='voter_question')  # 추천인 추가
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posting')
    scraper = models.ManyToManyField(User, related_name='scrap_posting')  # through는 연결할 모델을 의미한다.
    scrap_counter = models.IntegerField(default=0)  # 불필요한 연산 없이 진행하기 위해.
    logo = models.URLField(max_length=200)



    def __str___(self):
        return self.subject

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True, blank=True)
    Posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    content = models.TextField()
    create_date = models.DateTimeField()
