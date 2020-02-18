from django.urls import path
from api import views

urlpatterns = [
    path('sns/', views.SNSView.as_view()),
]
