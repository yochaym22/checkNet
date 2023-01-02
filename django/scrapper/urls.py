from django.urls import path
from . import views

#url conf
urlpatterns = [
    path('game/<int:game_number>', views.scrap)
]