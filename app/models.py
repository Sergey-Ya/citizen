from django.db import models


class CostGroup(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

class Cost(models.Model):
    costgroup = models.ForeignKey(CostGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    cost = models.IntegerField()
    default = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)



class Order(models.Model):
    created_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


class Price(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)

    # tabletop from Cupboard
    tabletop_cost_id = models.ForeignKey(Cost, related_name='tabletop_cost', on_delete=models.CASCADE, null=True)

    tabletopend = models.IntegerField(default=0)
    tabletopend_cost_id = models.ForeignKey(Cost, related_name='tabletopend_cost', on_delete=models.CASCADE, null=True)

    tabletopedge = models.IntegerField(default=0)
    tabletopedge_cost_id = models.ForeignKey(Cost, related_name='tabletopedge_cost_id', on_delete=models.CASCADE, null=True)

    plinth = models.IntegerField(default=0)
    plinth_cost_id = models.ForeignKey(Cost, related_name='plinth_cost_id', on_delete=models.CASCADE, null=True)

    plinthcap = models.IntegerField(default=0)
    plinthcap_cost_id = models.ForeignKey(Cost, related_name='plinthcap_cost_id', on_delete=models.CASCADE, null=True)

    wallpanel = models.IntegerField(default=0)
    wallpanel_cost_id = models.ForeignKey(Cost, related_name='wallpanel_cost_id', on_delete=models.CASCADE, null=True)

    wallcap = models.IntegerField(default=0)
    wallcap_cost_id = models.ForeignKey(Cost, related_name='wallcap_cost_id', on_delete=models.CASCADE, null=True)

    # loop from Cupboard
    loop_cost_id = models.ForeignKey(Cost, related_name='loop_cost_id', on_delete=models.CASCADE, null=True)

    # handle from Cupboard
    handle_cost_id = models.ForeignKey(Cost, related_name='handle_cost_id', on_delete=models.CASCADE, null=True)

    # hitch from Cupboard
    hitch_cost_id = models.ForeignKey(Cost, related_name='hitch_cost_id', on_delete=models.CASCADE, null=True)

    rail = models.IntegerField(default=0)
    rail_cost_id = models.ForeignKey(Cost, related_name='rail_cost_id', on_delete=models.CASCADE, null=True)

    # baguette from Cupboard
    baguette_cost_id = models.ForeignKey(Cost, related_name='baguette_cost_id', on_delete=models.CASCADE, null=True)

    # roof from Cupboard
    roof_cost_id = models.ForeignKey(Cost, related_name='roof_cost_id', on_delete=models.CASCADE, null=True)

    baluster = models.IntegerField(default=0)
    baluster_cost_id = models.ForeignKey(Cost, related_name='baluster_cost_id', on_delete=models.CASCADE, null=True)

    socle = models.IntegerField(default=0)
    socle_cost_id = models.ForeignKey(Cost, related_name='socle_cost_id', on_delete=models.CASCADE, null=True)

    drying = models.IntegerField(default=0)
    drying_cost_id = models.ForeignKey(Cost, related_name='drying_cost_id', on_delete=models.CASCADE, null=True)

    backlight = models.IntegerField(default=0)
    backlight_cost_id = models.ForeignKey(Cost, related_name='backlight_cost_id', on_delete=models.CASCADE, null=True)

    # facade from Cupboard
    facade_cost_id = models.ForeignKey(Cost, related_name='facade_cost_id', on_delete=models.CASCADE, null=True)

    # facadeskin from Cupboard
    facadeskin_cost_id = models.ForeignKey(Cost, related_name='facadeskin_cost_id', on_delete=models.CASCADE, null=True)

    # facadeskingl from Cupboard
    facadeskingl_cost_id = models.ForeignKey(Cost, related_name='facadeskingl_cost_id', on_delete=models.CASCADE, null=True)

    # facadeplastic from Cupboard
    facadeplastic_cost_id = models.ForeignKey(Cost, related_name='facadeplastic_cost_id', on_delete=models.CASCADE, null=True)

    facadeskintype = models.IntegerField(default=0)

    othercost = models.IntegerField(default=0)


class CupboardLst(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    tabletop = models.IntegerField(default=0)
    hz = models.IntegerField(default=0)
    skin = models.IntegerField(default=0)
    skingl = models.IntegerField(default=0)
    plastic = models.IntegerField(default=0)
    facade = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    loop = models.IntegerField(default=0)
    hitch = models.IntegerField(default=0)
    roof = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    baguette = models.IntegerField(default=0)
    handle = models.IntegerField(default=0)

class Cupboard(models.Model):
    cupboardlst_id = models.ForeignKey(CupboardLst, on_delete=models.CASCADE, default=0)
    price_id = models.ForeignKey(Price, on_delete=models.CASCADE, default=0)
    count = models.IntegerField(default=0)


