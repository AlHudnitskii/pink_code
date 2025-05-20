from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtaionPairView, RegisterView, LogoutView, LoginView


app_name = "auth_"

urlpatterns = [
    path("token/", MyTokenObtaionPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
]