from django.urls import path
from .views import scrape_audio, list_audios, get_audio, delete_audio

urlpatterns = [
    path('', scrape_audio, name='scrap_audio'),
    path('audios/', list_audios, name='list_audios'),
    path('audios/<int:pk>/', get_audio, name='get_audio'),
    path('audios_delete/<int:pk>/', delete_audio, name='delete_audio'),
]