from django.db import models

# Create your models here.


class Quote(models.Model):
    text = models.CharField(max_length=255) # 명언 내용
    author = models.CharField(max_length=100) # 명언의 저자

    def __str__(self):
        return f"{self.text} - {self.author}"