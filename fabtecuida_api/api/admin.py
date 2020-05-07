from django.contrib import admin
from .models import Item, Entity, Order, OrderRequestedItem, OrderSuppliedItem, SupplierInventory

admin.site.register(Item)
admin.site.register(Entity)
admin.site.register(Order)
admin.site.register(OrderRequestedItem)
admin.site.register(OrderSuppliedItem)
admin.site.register(SupplierInventory)
