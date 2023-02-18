from django.db import models
from django.contrib.auth.models import User


class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tittle = models.CharField(max_length=200)
    discription = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tittle

    def question_answer(self):
        self.answers_set.all()


class Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=500)
    upvote = models.ManyToManyField(User, related_name='upvote', )

    def __str__(self):
        return self.answer

    @property
    def upvote_count(self):
        return self.upvote.all().count()
