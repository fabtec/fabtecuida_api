from django.conf.urls import url, include
from django.urls import path
from rest_framework_simplejwt.views import (
	TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'api/entities', views.EntityViewSet)
router.register(r'api/items', views.ItemViewSet)
# router.register(r'api/orders', OrderViewSet)
#router.register(r'api/suppliers',SupplierInventoryViewSet)
# router.register(r'api/orders-requested',OrderRequestedItemViewSet)
router.register(r'api/orders-supplied', views.OrderSuppliedItemViewSet)
router.register(r'api/users', views.UserViewSet)
# router.register(r'api/supplier-inventory',SupplierInventoryViewSet)



urlpatterns = [
	url(r'^', include(router.urls)),
	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
	path('api/token/user/',views.GetUserViewSet.as_view(), name='obtain_user_with_token'),
	# path('api/items/', ItemAPIView.as_view()),
	# path('api/entities/', EntityAPIView.as_view()),
	# url('api/orders/(?P<pk>[\w-]+)/', OrderViewSet.as_view(), name='orders'),

	path('api/orders-requested/', views.OrderRequestedItemViewSet.as_view(), name='orders-requested-list'),
	path('api/orders-requested/<int:pk>/', views.OrderRequestedItemViewSet.as_view(), name='orders-requested-detail'),
	path('api/orders/', views.OrderViewSet.as_view(), name='orders-list'),
	path('api/orders/<int:pk>/', views.OrderViewSet.as_view(), name='orders-detail'),
	path('api/supplied-item/', views.SuppliedItemViewSet.as_view(), name='supplied-item'),
	path('api/create-orders/', views.CreateOrderAdminViewSet.as_view(), name='create-order'),
	path('api/entities/', views.EntityViewSet.as_view(), name='entities'),
	path('api/supplier-inventory/', views.SupplierInventoryViewSet.as_view(), name='supplier-inventory')
	
]
