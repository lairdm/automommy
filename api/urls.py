from django.urls import path
from api.views import sns, launcher

urlpatterns = [
    path('sns/', sns.SNSView.as_view()),
    path('launch/<show>/<location>/', launcher.Launcher.as_view())
]
