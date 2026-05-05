from django.urls import path, include
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from accounts.views import GoogleLogin, UserViewSet, ProfileView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("profile/", ProfileView.as_view(), name="rest_user_details"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("", include(router.urls)),
]
