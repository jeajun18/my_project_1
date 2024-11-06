import random

from django.http import JsonResponse
from django.shortcuts import render
from .models import Quote

# Create your views here.


def random_quote(request):
    quotes = Quote.objects.all()
    if quotes:
        quote = random.choice(quotes)
        data = {
            "text" : quote.text,
            "author" : quote.author,
            "category" : quote.category.name,
        }
    else:
        data = {
            "text" : "No quotes available",
            "author" : "",
        }

    return JsonResponse(data)


def random_quote_by_category(request, category_id):
    # 선택된 카테고리에 속한 모든 Quote 객체를 필터링하여 가져옵니다.
    quotes = Quote.objects.filter(category_id=category_id)
    # 만약 quotes 가 존재하면
    if quotes:
        # quotes 목록에서 랜덤으로 하나를 선택.
        quote = random.choice(quotes)
        # 선택된 quote 객체의 정보를 딕셔너리 형태로 구성.
        data = {
            "text" : quote.text,    # 선택된 Quote의 텍스트
            "author" : quote.author,    # 선택된 Quote의 저자
            "category" : quote.category.name,   # 선택된 Quote의 카테고리 이름
        }
    # quotes 가 없을 때, 없다는 메시지를 전달.
    else:
        data ={
            "text" : "No quotes available for this category",
            "author" : "",
        }
    # 구성된 데이터를 JSON 형식으로 응답
    return JsonResponse(data)