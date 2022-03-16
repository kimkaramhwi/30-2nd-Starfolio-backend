from django.urls import path

from users.views import KakaoLogInView

urlpatterns = [
    path('/kakao-login', KakaoLogInView.as_view()),
]

