from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from authenticate.views import (
    IndexView,
    UserLoginView,
    UserLogoutView,
    UserRegistrationView,
    profile
)

app_name = 'auth'

urlpatterns = [
    # Authentication URLs
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('', IndexView.as_view(), name='index'),

    # JWT Token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token-verify'),
]
