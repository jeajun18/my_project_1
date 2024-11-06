import random

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import QuoteForm
from .models import Favorite, Quote

# Create your views here.


def random_quote(request):
    quotes = Quote.objects.all()
    if quotes:
        quote = random.choice(quotes)
        data = {
            "text": quote.text,
            "author": quote.author,
            "category": quote.category.name,
        }
    else:
        data = {
            "text": "No quotes available",
            "author": "",
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
            "text": quote.text,  # 선택된 Quote의 텍스트
            "author": quote.author,  # 선택된 Quote의 저자
            "category": quote.category.name,  # 선택된 Quote의 카테고리 이름
        }
    # quotes 가 없을 때, 없다는 메시지를 전달.
    else:
        data = {
            "text": "No quotes available for this category",
            "author": "",
        }
    # 구성된 데이터를 JSON 형식으로 응답
    return JsonResponse(data)


def like_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return JsonResponse({"like": quote.likes})


def add_to_favorites(request, quote_id):
    # 현재 로그인한 사용자를 request.user로부터 가져온다.
    # 만약 로그인하지 않은 경우 request.user 는 AnonymousUser 객체로 설정된다.
    user = request.user
    # quote_id 에 해당하는 인용문을 데이터베이스에서 검색한다.
    # quote_id 에 해당하는 Quote 객체를 검색하고, 만약 해당 인용문을 찾지 못하면, Http404 오류를 발생시킨다.
    # 즉, quote_id가 존재하는 Quote 객체가 없으면 404오류 페이지를 반환한다.
    quote = get_object_or_404(Quote, id=quote_id)
    # Favorite 모델을 사용하여 명언 간의 즐겨찾기 관계를 생성한다.
    # user와 quote가 일치하는 Favorite 객체가 있는지 확인한다.
    # 만약 그런 객체가 없다면, 새로운 Favorite 객체를 생성하고 저장한다.
    # 만약 이미 존재하는 객체가 있다면 그 객체를 그대로 반환한다.
    # 중복된 즐겨찾기가 생성되지 않도록 보장한다. 즉, 같은 사용자가 동일한 명언을 여러번 즐겨찾기에 추가하는 것을 방지한다.
    Favorite.objects.get_or_create(user=user, quote=quote)
    return JsonResponse({"message": "Quote added to favorites"})


def add_quote(request):
    # 만약 POST 요청을 받는다면.
    if request.method == "PSOT":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            # 명언 목록 페이지로 리다이렉트
            return redirect("quote_list")
    else:
        form = QuoteForm()
    return render(request, "quotes/add_quote.html", {"form": form})


def recommended_quotes(request):
    # 좋아요 수가 많은 명언이 먼저 오도록 정의된다. 상위 5개만.
    top_quotes = Quote.objects.order_by("-likes")[:5]
    data = [
        # top_quotes 에서 가져온 명언들을 하나씩 순회하며, 각 명언에 대해 텍스트, 저자, 좋아요 수 를 딕셔너리 형식으로 저장한 리스트를 생성
        # 이 리스트는 추천 명언 정보를 포함하여, 각 명언에 대한 기본적인 정보만을 포함한 딕셔너리로 구성된다.
        {"text": quote.text, "author": quote.author, "likes": quote.likes}
        for quote in top_quotes
    ]
    # data : 위에서 생성된 추천 명언들의 리스트
    # safe=False : 기본적으로 JsonResponse는 딕셔너리 형식의 데이터를 JSON으로 변환하는데,
    # 리스트는 안전하게 변환이 가능하기 때문에 safe=False 설정을 해줘야한다.
    return JsonResponse(data, safe=False)
