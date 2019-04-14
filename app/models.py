from django.db import models


class Order(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class Price(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    tabletop_end = models.IntegerField(default=0)
    tabletop_edge = models.IntegerField(default=0)
    plinth = models.IntegerField(default=0)
    plinth_cap = models.IntegerField(default=0)
    wall_panel = models.IntegerField(default=0)
    wall_cap = models.IntegerField(default=0)
    rail = models.IntegerField(default=0)
    baluster = models.IntegerField(default=0)
    socle = models.IntegerField(default=0)
    drying = models.IntegerField(default=0)
    backlight = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    counttabletop = None
    countloop = None
    counthandle = None
    counthitch = None
    countbaguette = None
    countroof = None
    countfacade = None
    countfacadeskin = None
    countfacadeskingl = None
    countfacadeplastic = None

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
    default = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
