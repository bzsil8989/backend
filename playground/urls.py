from django.urls import path
from .views import chatbot_view, chatbot

urlpatterns = [
    path('', chatbot_view, name='chatbot-home'),  # Serve chatbot.html at the root URL
    path('chatbot/', chatbot, name='chatbot'),  # API for chatbot communication
]