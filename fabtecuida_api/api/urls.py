from django.conf.urls import url, include
from django.urls import path
from rest_framework_simplejwt.views import (
	TokenObtainPairView, TokenRefreshView, TokenVerifyView
)
# from .views import EntityAPIView, ItemAPIView, OrderAPIView
from .views import UserViewSet, EntityViewSet, ItemViewSet, OrderViewSet, SupplierInventoryViewSet, OrderRequestedItemViewSet, OrderSuppliedItemViewSet, SupplierInventoryViewSet, SuppliedItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api/entities', EntityViewSet)
router.register(r'api/items', ItemViewSet)
# router.register(r'api/orders', OrderViewSet)
#router.register(r'api/suppliers',SupplierInventoryViewSet)
# router.register(r'api/orders-requested',OrderRequestedItemViewSet)
router.register(r'api/orders-supplied',OrderSuppliedItemViewSet)
router.register(r'api/users',UserViewSet)
router.register(r'api/supplier-inventory',SupplierInventoryViewSet)



urlpatterns = [
	url(r'^', include(router.urls)),
	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
	
	# path('api/items/', ItemAPIView.as_view()),
	# path('api/entities/', EntityAPIView.as_view()),
	# url('api/orders/(?P<pk>[\w-]+)/', OrderViewSet.as_view(), name='orders'),

	path('api/orders-requested/', OrderRequestedItemViewSet.as_view(), name='orders-requested-list'),
	path('api/orders-requested/<int:pk>/', OrderRequestedItemViewSet.as_view(), name='orders-requested-detail'),
	path('api/orders/', OrderViewSet.as_view(), name='orders-list'),
	path('api/orders/<int:pk>/', OrderViewSet.as_view(), name='orders-detail'),
	path('api/supplied-item/', SuppliedItemViewSet.as_view(), name='supplied-item'),

]
