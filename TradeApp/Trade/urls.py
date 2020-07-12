from django.urls import path
from .views import Trade

urlpatterns = [
    path('currency/<symbol>/', Trade.as_view()),
    path('currency/all/', Trade.as_view()),
    path('currency/symbol/',Trade.as_view())
]