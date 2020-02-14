from django.urls import path
from .views import *

urlpatterns = [
    path('meets/', MeetsView.as_view()),
    path('meets/propose/', ProposeMeetView.as_view()),
    path('meets/<int:pk>/', MeetView.as_view()),
    path('meets/<int:pk>/fill-response/', FillResponseView.as_view()),
    path('meets/<int:pk>/add-members/', AddMembersView.as_view()),
    path('meets/<int:pk>/check-response/', CheckResponseView.as_view()),
    path('meets/<int:pk>/finalize-meet/', FinalizeMeetView.as_view()),
    path('meets/<int:pk>/add-task/', AddTaskView.as_view()),
    path('task/<int:pk>/complete/', CompleteTaskView.as_view())
]