from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('play/<str:game_type>/', views.play_game, name='play_game'),
    path('save-score/', views.save_score, name='save_score'),
] 