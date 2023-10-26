from django.urls import path
from . import views

urlpatterns = [
    path('api/chat_messages/', views.voice_input, name='chat-messages-list'),
    path('api/text_to_vioce/', views.text_to_voice, name='text-to-voice'),
    # Add more API endpoints here...
]
