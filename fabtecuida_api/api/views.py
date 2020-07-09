from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from .models import Item, Entity, Order, OrderRequestedItem, OrderSuppliedItem, SupplierInventory
from .serializers import ItemSerializer, EntitySerializer, OrderSerializer, OrderRequestedItemSerializer, OrderSuppliedItemSerializer, SupplierInventorySerializer


class EntityViewSet(viewsets.ModelViewSet):
	queryset         = Entity.objects.all()
	serializer_class = EntitySerializer

class ItemViewSet(viewsets.ModelViewSet):
	queryset         = Item.objects.all()
	serializer_class = ItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
	queryset         = Order.objects.all()
	serializer_class = OrderSerializer

class OrderRequestedItemViewSet(viewsets.ModelViewSet):
	queryset         = OrderRequestedItem.objects.all()
	serializer_class = OrderRequestedItemSerializer

class OrderSuppliedItemViewSet(viewsets.ModelViewSet):
	queryset         = OrderSuppliedItem.objects.all()
	serializer_class = OrderSuppliedItemSerializer

class SupplierInventoryViewSet(viewsets.ModelViewSet):
	queryset         = SupplierInventory.objects.all()
	serializer_class = SupplierInventorySerializer

#################### CUSTOM API ####################


class ItemAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		items = Item.objects.all()
		serializer = ItemSerializer(items, many=True)
		return Response(serializer.data)

class EntityAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entities = Entity.objects.all()
        serializer = EntitySerializer(entities, many=True)
        return Response(serializer.data)

class OrderAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data
		data['requester'] = request.user.id

		serializer = OrderSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
