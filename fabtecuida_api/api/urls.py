from django.conf.urls import url, include
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
# from .views import EntityAPIView, ItemAPIView, OrderAPIView
from .views import EntityViewSet, ItemViewSet, OrderViewSet, SupplierInventoryViewSet, OrderRequestedItemViewSet, OrderSuppliedItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/entities', EntityViewSet)
router.register(r'api/items', ItemViewSet)
router.register(r'api/orders', OrderViewSet)
router.register(r'api/suppliers',SupplierInventoryViewSet)
router.register(r'api/orders-requested',OrderRequestedItemViewSet)
router.register(r'api/orders-supplied',OrderSuppliedItemViewSet)


urlpatterns = [
	url(r'^', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/items/', ItemAPIView.as_view()),
    # path('api/entities/', EntityAPIView.as_view()),
    # path('api/orders/', OrderAPIView.as_view(), name='orders'),
]
