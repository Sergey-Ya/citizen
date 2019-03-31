from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import dateformat, timezone
from django.conf import settings

from .models import Order, Price, Base, Cupboard

from datetime import datetime
import json



def ajax_view(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action')
            rp = request.POST

            if action == 'save_order':
                now = datetime.now()
                newOrder = Order(name=rp.get('name'), comment=rp.get('comment'), created_at=now)
                newOrder.save()
                now = dateformat.format(now, settings.DATE_FORMAT)
                return HttpResponse(json.dumps({'id': newOrder.id, 'created_at': now}), content_type='application/json')


        else:
            return HttpResponse(json.dumps({'no': 'no'}), content_type='application/json')

    except Exception as e:
        return HttpResponse(Exception(e), status=400)




def home_view(request):
    return render(request, 'home.html', {})


def orders_view(request):
    return render(request, 'orders.html', {'orderlst': Order.objects.all().order_by('-id')})


def order_info_view(request, orderid):
    from django.db.models import Sum

    priced = Price.objects.filter(order_id=orderid).values()
    cupboardlst = Cupboard.objects.filter(price_id=priced.values('id')[0]['id'])

    counttabletop = 0
    countloop = 0
    counthandle = 0
    counthitch = 0
    countbaguette = 0
    countroof = 0
    countfacade = 0
    for coupboard in cupboardlst:
        counttabletop += coupboard.count * coupboard.base_id.tabletop
        countloop += coupboard.count * coupboard.base_id.loop
        counthandle += coupboard.count * coupboard.base_id.handle
        counthitch += coupboard.count * coupboard.base_id.hitch
        countbaguette += coupboard.count * coupboard.base_id.baguette
        countroof += coupboard.count * coupboard.base_id.roof
        countfacade += coupboard.count * coupboard.base_id.facade


    for price in priced:
        # counttabletop = cupboardlst.aggregate(Sum('count'))['count__sum'] * \
        #                 cupboardlst.aggregate(Sum('base_id__tabletop'))['base_id__tabletop__sum']
        price["counttabletop"] = counttabletop * 0.001
        price["countloop"] = countloop
        price["counthandle"] = counthandle
        price["counthitch"] = counthitch
        price["countbaguette"] = countbaguette * 0.001
        price["countroof"] = countroof
        price["countfacade"] = countfacade



    return render(request, 'order_info.html', {'price': priced, 'cupboardlst': cupboardlst})

