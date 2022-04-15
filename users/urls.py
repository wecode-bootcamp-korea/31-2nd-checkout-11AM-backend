from django.urls import path

from .views import GetUserInfoView

urlpatterns = [
    path('/kakao/callback', GetUserInfoView.as_view()),
]