from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from .models import Item, Entity, Order, OrderRequestedItem, OrderSuppliedItem, SupplierInventory
from .serializers import ItemSerializer, EntitySerializer, OrderSerializer, CreateOrderSerializer, OrderRequestedItemSerializer, CreateOrderRequestedItemSerializer, OrderSuppliedItemSerializer, SupplierInventorySerializer, UserSerializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
	queryset         = User.objects.all()
	serializer_class = UserSerializer

class EntityViewSet(viewsets.ModelViewSet):
	queryset         = Entity.objects.all()
	serializer_class = EntitySerializer

class ItemViewSet(viewsets.ModelViewSet):
	queryset         = Item.objects.all()
	serializer_class = ItemSerializer

class OrderViewSet(APIView):
	# authentication_classes = [JWTAuthentication]
	# permission_classes = [IsAuthenticated]

	def get(self, request):
		orders = Order.objects.all()
		serializer = OrderSerializer(orders, many=True)
		return Response(serializer.data)

	def post(self, request):
		# data = request.data
		#data['requester'] = request.user.id

		serializer = CreateOrderSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def put(self, request, *args, **kwargs):
	# 	order = self.get_object(self.POST.get['pk'])
	#	serializer = CreateOrderSerializer(order, data=request.data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def delete(self, request, *args, **kwargs):
	# 	order = self.get_object(self.POST.get['pk'])
	# 	order.delete()
	# 	return Response(status=status.HTTP_204_NO_CONTENT)


# class OrderRequestedItemViewSet(viewsets.ModelViewSet):
# 	queryset         = OrderRequestedItem.objects.all()
# 	serializer_class = OrderRequestedItemSerializer

class OrderRequestedItemViewSet(APIView):
	# authentication_classes = [JWTAuthentication]
	# permission_classes = [IsAuthenticated]

	def get(self, request):
		orders = OrderRequestedItem.objects.all()
		serializer = OrderRequestedItemSerializer(orders, many=True)
		return Response(serializer.data)

	def post(self, request):
		# data = request.data
		#data['requester'] = request.user.id

		serializer = CreateOrderRequestedItemSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def put(self, request, *args, **kwargs):
	# 	order = self.get_object(self.POST.get['pk'])
	#	serializer = CreateOrderRequestedItemSerializer(order, data=request.data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# def delete(self, request, *args, **kwargs):
	# 	order = self.get_object(self.POST.get['pk'])
	# 	order.delete()
	# 	return Response(status=status.HTTP_204_NO_CONTENT)
	


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
