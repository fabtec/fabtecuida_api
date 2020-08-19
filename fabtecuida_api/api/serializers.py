from rest_framework import serializers
from .models import Item, Entity, Order, OrderRequestedItem, OrderSuppliedItem, SupplierInventory
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = [
			'id',
			'last_login',
			'username',
			'first_name',
			'last_name',
			'email',
			'date_joined'
		]

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = ['id', 'name', 'description']

class EntitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Entity
		fields = ['id', 'name', 'location', 'manager']

#FILTRO DE ORDENES 1)ENTIDADES__ID, 2)STATUS, 3)QUANTITY lt210 y gt (>=), 4)TIPO
#localhost:8000/api/orders/?entity=1203&status="INPROGRESS"&quantity=lt210&type="SUPPLIED"
#STATUS //PENDING - DONE - INPROGRESS (POR FRONT)		
#TYPES SUPPLIED - REQUESTED									

# class OrderRequestedItemSerializer(serializers.ModelSerializer):
# 	order = OrderSerializer()
# 	class Meta:
# 		model = OrderRequestedItem
# 		fields = '__all__'

class BaseOrderRequestedItemSerializer(serializers.ModelSerializer):
	item  = ItemSerializer()
	date  = serializers.DateTimeField(source='created_at')
	class Meta:
		model = OrderRequestedItem
		fields = [
			'id',
			'item',
			'status',
			'quantity',
			'date',
			'updated_at',
		]

class BaseOrderSuppliedItemSerializer(serializers.ModelSerializer):
	item  = ItemSerializer()
	supplier = EntitySerializer()
	date  = serializers.DateTimeField(source='created_at')
	class Meta:
		model = OrderRequestedItem
		fields = [
			'id',
			'supplier',
			'item',
			'status',
			'quantity',
			'date',
			'updated_at',
		]

class BaseOrderSerializer(serializers.ModelSerializer):
	# order_requested_item = OrderRequestedItemSerializer(source='getOrdersRequested', many=True)
	# order_supplied_item  = OrderSuppliedItemSerializer(source='getOrdersSupplied', many=True)
	date      = serializers.DateTimeField(source='created_at')
	requester = UserSerializer()
	entity    = EntitySerializer()
	class Meta:
		model = Order
		fields = [
			'id',
			'requester',
			'entity',
			'status',
			# 'order_requested_item',
			# 'order_supplied_item',
			'date',
			'updated_at'
		]

class OrderSerializer(serializers.ModelSerializer):
	order_requested_item = BaseOrderRequestedItemSerializer(source='getOrdersRequested', many=True)
	order_supplied_item  = BaseOrderSuppliedItemSerializer(source='getOrdersSupplied', many=True)
	date                 = serializers.DateTimeField(source='created_at')
	requester            = UserSerializer()
	entity               = EntitySerializer()
	class Meta:
		model  = Order
		fields = [
			'id',
			'requester',
			'entity',
			'order_requested_item',
			'order_supplied_item',
			'date',
			'status',
			'updated_at'
		]

class CreateOrderSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Order
		fields = '__all__'

class OrderRequestedItemSerializer(serializers.ModelSerializer):
	order = BaseOrderSerializer()
	item  = ItemSerializer()
	date  = serializers.DateTimeField(source='created_at')
	class Meta:
		model = OrderRequestedItem
		fields = [
			'order',
			'item',
			'status',
			'quantity',
			'date',
			'updated_at',
		]

class CreateOrderRequestedItemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = OrderRequestedItem
		fields = '__all__'

class OrderSuppliedItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderSuppliedItem
		fields = '__all__'

class SupplierInventorySerializer(serializers.ModelSerializer):
	supplier = EntitySerializer()
	item     = ItemSerializer()
	class Meta:
		model = SupplierInventory
		fields = '__all__'