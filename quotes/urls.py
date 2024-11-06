from django.urls import path

from . import views

urlpatterns = [
    path('random/', views.random_quote, name='random_quote'),
    path('random/<int:category_id>/', views.random_quote_by_category, name="random_quote_by_category")
]

