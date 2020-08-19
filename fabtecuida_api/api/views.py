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
from django.dispatch import receiver
from django.db.models.signals import post_save

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


class OrderSuppliedItemViewSet(viewsets.ModelViewSet):
	queryset         = OrderSuppliedItem.objects.all()
	serializer_class = OrderSuppliedItemSerializer

#################### CUSTOM API ####################

class OrderViewSet(APIView):
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

						if('quantity' in request.GET):
							if(request.GET['quantity']!=""):
								orders = orders.filter(order_requested__quantity__gte=request.GET['quantity'] )

					elif(request.GET['type']=="SUPPLIED"):
						orders = orders.exclude(order_supplied__pk__isnull=True)
							
						if('quantity' in request.GET):
							if(request.GET['quantity']!=""):
								orders = orders.filter(order_supplied__quantity__gte=request.GET['quantity'] )	
			
				serializer = OrderSerializer(orders, many=True)
				
			
		return Response(serializer.data)

	def post(self, request):
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


class OrderRequestedItemViewSet(APIView):

	def get(self, request):
		orders = OrderRequestedItem.objects.all()
		serializer = OrderRequestedItemSerializer(orders, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = CreateOrderRequestedItemSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuppliedItemViewSet(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]
	
	def post(self, request):
		data = request.data
		
		if "itemSelected" in data and "requested_item" in data:
			requested_item = OrderRequestedItem.objects.get(pk=data['requested_item'])

			for item_selected in data['itemSelected']:
				item_inventory = SupplierInventory.objects.get(pk=item_selected)
				supplied_quantity = item_inventory.quantity - requested_item.quantity
				
				if supplied_quantity > 0:
					item_inventory.quantity = item_inventory.quantity - requested_item.quantity
					item_inventory.save()
					requested_item.quantity = 0
					requested_item.status = "INPROGRESS"
				elif supplied_quantity == 0:
					requested_item.quantity = 0
					requested_item.status = "INPROGRESS"
					item_inventory.delete()
				else:
					requested_item.quantity = requested_item.quantity - item_inventory.quantity
					requested_item.status = "PENDING"
					item_inventory.delete()

				OrderSuppliedItem.objects.create(
					order = requested_item.order,
					supplier = item_inventory.supplier,
					item = requested_item.item,
					status = "INPROGRESS",
					quantity = supplied_quantity
				)

				requested_item.save()
			
			#si no hay mas items en PENDING, PASAR ORDEN A INPROGRESS

			#recorrer la orden
			#recorrer todos los items en busca de un status PENDING
			#Si No existe ningun pending cambiar status de orden a INPROGRESS
			count_pending = 0
			for	requested_item_tmp in requested_item.order.getOrdersRequested():
				if requested_item_tmp.status == "PENDING":
					count_pending =  count_pending + 1
			
			if count_pending == 0:
				requested_item.order.status = "INPROGRESS"
				requested_item.order.save()
				
			return Response({'response': 'Guardado Correctamente'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'response': 'itemSelected & requested_item required'}, status=status.HTTP_400_BAD_REQUEST)

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

#REVISANDO DESPUÉS DE GUARDAR
@receiver(post_save, sender=OrderSuppliedItem)
def post_save_order_supplied_item(sender, instance, **kwargs):
	count_pending = 0
	for	supplied_item_tmp in instance.order.getOrdersSupplied():
		if supplied_item_tmp.status != "DONE":
			count_pending =  count_pending + 1
	
	if count_pending == 0:
		instance.order.status = "DONE"
		instance.order.save()

		for	requested_item_tmp in instance.order.getOrdersRequested():
			requested_item_tmp.status = "DONE"
			requested_item_tmp.save()