from rest_framework import serializers
from .models import Item, Entity, Order, OrderRequestedItem, OrderSuppliedItem, SupplierInventory

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'name', 'location']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderRequestedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequestedItem
        fields = '__all__'

class OrderSuppliedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSuppliedItem
        fields = '__all__'

class SupplierInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierInventory
        fields = '__all__'
