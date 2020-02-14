from django.urls import path,include
from .views import *
urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('admin/token/', GetTokenView.as_view()),
]