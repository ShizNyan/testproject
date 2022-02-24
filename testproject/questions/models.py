import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    author = models.CharField(max_length=200)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(default=0)
    solution = models.BooleanField(default=False)
    tags = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    def published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    answer_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    rating = models.IntegerField(default=0)
    solution = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
