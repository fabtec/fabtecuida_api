from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
from .views import EntityAPIView, ItemAPIView, OrderAPIView


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/items/', ItemAPIView.as_view()),
    path('api/entities/', EntityAPIView.as_view()),
    path('api/orders/', OrderAPIView.as_view()),
]
