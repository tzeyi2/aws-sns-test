from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('market_data/bloomberg/', views.receive_bloomberg_sns_message,
         name="receive_bloomberg_sns_message"),
]
