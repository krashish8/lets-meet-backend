from django.urls import path
from .views import *

urlpatterns = [
    path('meets/', MeetsView.as_view()),
    path('meets/propose/', ProposeMeetView.as_view()),
    path('meets/<int:pk>/', MeetView.as_view()),
]