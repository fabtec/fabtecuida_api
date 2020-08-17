from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from .models import Item, Entity, Order, OrderRequestedItem, OrderSuppliedItem, SupplierInventory
from .serializers import SupplierInventorySerializer, ItemSerializer, EntitySerializer, OrderSerializer, CreateOrderSerializer, OrderRequestedItemSerializer, CreateOrderRequestedItemSerializer, OrderSuppliedItemSerializer, SupplierInventorySerializer, UserSerializer, BaseOrderSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserViewSet(viewsets.ModelViewSet):
	queryset         = User.objects.all()
	serializer_class = UserSerializer

class EntityViewSet(viewsets.ModelViewSet):
	queryset         = Entity.objects.all()
	serializer_class = EntitySerializer

class ItemViewSet(viewsets.ModelViewSet):
	queryset         = Item.objects.all()
	serializer_class = ItemSerializer

class SupplierInventoryViewSet(viewsets.ModelViewSet):
	queryset         = SupplierInventory.objects.all()
	serializer_class = SupplierInventorySerializer
	filter_backends  = [DjangoFilterBackend]
	filterset_fields = ['item']

class OrderViewSet(APIView):
	# authentication_classes = [JWTAuthentication]
	# permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		if 'pk' in kwargs:
			orders = Order.objects.get(pk=int(kwargs['pk']))
			serializer = OrderSerializer(orders)

		else:
			orders = Order.objects.all()
			serializer = OrderSerializer(orders, many=True)

			if('entity' in request.GET):
				if(request.GET['entity']!=""):
					orders = orders.filter(entity__id=request.GET['entity'] )

				if('status' in request.GET):
					if(request.GET['status']!=""):
						orders = orders.filter(status=request.GET['status'] )
						

				serializer = OrderSerializer(orders, many=True)

			if('type' in request.GET):
				if(request.GET['type']!=""):
					if(request.GET['type']=="REQUESTED"):
						orders = orders.exclude(order_requested__pk__isnull=True)
						# if('status' in request.GET):
						# 	if(request.GET['status']!=""):
						# 		orders = orders.filter(order_requested__status=request.GET['status'] )

						if('quantity' in request.GET):
							if(request.GET['quantity']!=""):
								orders = orders.filter(order_requested__quantity__gte=request.GET['quantity'] )

					elif(request.GET['type']=="SUPPLIED"):
						orders = orders.exclude(order_supplied__pk__isnull=True)
						# if('status' in request.GET):
						# 	if(request.GET['status']!=""):
						# 		orders = orders.filter(order_supplied__status=request.GET['status'] )
							
						if('quantity' in request.GET):
							if(request.GET['quantity']!=""):
								orders = orders.filter(order_supplied__quantity__gte=request.GET['quantity'] )	
			
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

	def put(self, request, *args, **kwargs):
		order = self.get_object(kwargs['pk'])
		serializer = CreateOrderSerializer(order, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

""" class SupplierInventoryViewSet(viewsets.ModelViewSet):
	queryset         = SupplierInventory.objects.all()
	serializer_class = SupplierInventorySerializer """

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
