from django.urls import path
from .views import EntityAPIView, ItemAPIView

urlpatterns = [
    path('api/items/', ItemAPIView.as_view()),
    path('api/entities/', EntityAPIView.as_view()),
]
