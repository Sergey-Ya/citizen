from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class Price(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    tabletop_end = models.IntegerField()
    tabletop_edge = models.IntegerField()
    plinth = models.IntegerField()
    plinth_cap = models.IntegerField()
    wall_panel = models.IntegerField()
    wall_cap = models.IntegerField()
    rail = models.IntegerField()
    baluster = models.IntegerField()
    drying = models.IntegerField()
    backlight = models.IntegerField()
    counttabletop = None
    countloop = None
    counthandle = None
    counthitch = None
    countbaguette = None
    countroof = None
    countfacade = None

class Base(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    tabletop = models.IntegerField()
    hz = models.IntegerField()
    skin = models.IntegerField()
    skingl = models.IntegerField()
    plastic = models.IntegerField()
    facade = models.DecimalField(max_digits=6, decimal_places=3)
    loop = models.IntegerField()
    hitch = models.IntegerField()
    roof = models.DecimalField(max_digits=6, decimal_places=3)
    baguette = models.IntegerField()
    handle = models.IntegerField()

class Cupboard(models.Model):
    base_id = models.ForeignKey(Base, on_delete=models.CASCADE)
    price_id = models.ForeignKey(Price, on_delete=models.CASCADE)
    count = models.IntegerField()

class CostGroup(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

class Cost(models.Model):
    costgroup = models.ForeignKey(CostGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    cost = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
