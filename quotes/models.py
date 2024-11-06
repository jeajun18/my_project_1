from django.db import models

# Create your models here.

# 명언 모델에 카테고리 필드를 추가하여 주제를 지정할 수 있도록 한다.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Quote(models.Model):
    text = models.CharField(max_length=255) # 명언 내용
    author = models.CharField(max_length=100) # 명언의 저자

    # 다대일 관계를 정의, Quote와 Category 모델간의 ForeignKey 설정.
    # Category : 참고하고자 하는 다른 모델.
    # on_delete=models.CASCADE : Category 객체가 삭제될 때, 이 ForeignKey 필드와 연결된 모든 객체도 함께 삭제되도록 하는 옵션.
    # related_name='quotes' : Category 모델에서 현재 모델을 참조할 때 사용할 이름 정의.
    # 예를 들어, Category 객체에서 quotes를 사용하여 이 ForeignKey 필드가 연결된 모든 객체에 접근할 수 있음.
    # 예를 들어, category_instance.quotes.all() 을 통해 특정 카테고리에 속한 모든 현재 모델의 객체를 가져올 수 있음.
    # 이 관계는 현재 Quote(N: Many) - Category(1: One)로 설정되어 있으며,
    # 이를 통해 Category 모델에서 각 category 객체에 속하는 모델들을 쉽게 조회 가능
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quotes', default=1)



    def __str__(self):
        return f"{self.text} - {self.author}"