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
        }
    else:
        data = {
            "text" : "No quotes available",
            "author" : "",
        }

    return JsonResponse(data)