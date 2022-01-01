from django.urls import path
from api.views import sns, launcher, transmission

urlpatterns = [
    path('sns/', sns.SNSView.as_view()),
    path('launch/<show>/<location>/', launcher.Launcher.as_view()),
    path('transmission/fetch/', transmission.Transmission.as_view()),
    path('transmission/fetch/<torrent_id>/', transmission.Transmission.as_view()),
]
