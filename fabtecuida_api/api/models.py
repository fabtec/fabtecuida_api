from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField

class Item(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Entity(models.Model):
    name       = models.CharField(max_length=255)
    location   = LocationField(zoom=7, default=Point(0,0))
    manager    = models.ManyToManyField(User)
    address    = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#CREAR ABSTRACT USER
#agregar entidad a usuario (requerido)
#entity    = models.ForeignKey(Entity, on_delete=models.CASCADE)

# TODO add states-stages for orders
class Order(models.Model):
    requester  = models.ForeignKey(User, on_delete=models.CASCADE)
    entity     = models.ForeignKey(Entity, on_delete=models.CASCADE)
    status     = models.CharField(max_length=255, default="PENDING") #PENDING - DONE - INPROGRESS (POR FRONT)
    finish_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getOrdersRequested(self):
        return OrderRequestedItem.objects.filter(order=self)

    def getOrdersSupplied(self):
        return OrderSuppliedItem.objects.filter(order=self)

class OrderRequestedItem(models.Model):
    order       = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_requested')
    item        = models.ForeignKey(Item, on_delete=models.CASCADE)
    status      = models.CharField(max_length=255, default="PENDING") #PENDING - DONE - INPROGRESS (POR FRONT)
    quantity    = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

class OrderSuppliedItem(models.Model):
    order                     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_supplied')
    supplier                  = models.ForeignKey(Entity, on_delete=models.CASCADE)
    item                      = models.ForeignKey(Item, on_delete=models.CASCADE)
    status                    = models.CharField(max_length=255)
    external_shipment_id      = models.TextField(blank=True, null=True)
    external_shipment_company = models.TextField(blank=True, null=True)
    quantity                  = models.IntegerField()
    created_at                = models.DateTimeField(auto_now_add=True)
    updated_at                = models.DateTimeField(auto_now=True)

class SupplierInventory(models.Model):
    supplier      = models.ForeignKey(Entity, on_delete=models.CASCADE)
    item          = models.ForeignKey(Item, on_delete=models.CASCADE)
    #origin_supply = models.ForeignKey(OrderSuppliedItem, on_delete=models.CASCADE)
    quantity      = models.IntegerField()
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
