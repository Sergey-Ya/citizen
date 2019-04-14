from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import dateformat, timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from .models import Order, Price, Base, Cupboard, CostGroup, Cost

from datetime import datetime
import json

from app.magic import base



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

            if action == 'send_sms':
                base.send_sms(rp.get('phone'))
                return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')



            if action == 'set_defaultcost':
                cost_m = Cost.objects.get(id=rp.get('costid'))
                Cost.objects.filter(costgroup_id=cost_m.costgroup_id).update(default=False)
                Cost.objects.filter(id=rp.get('costid')).update(default=True)
                return HttpResponse(json.dumps(cost_m.costgroup_id), content_type='application/json')

            if action == 'add_cost':
                cost = Cost(name=rp.get('name'), cost=rp.get('cost'), costgroup_id=rp.get('param'))
                cost.save()
                return HttpResponse(json.dumps(cost.id), content_type='application/json')

            if action == 'edit_cost':
                Cost.objects.filter(id=rp.get('param')).update(name=rp.get('name'), cost=rp.get('cost'))
                return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')

            if action == 'del_cost':
                Cost.objects.filter(id=rp.get('costid')).delete()
                return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')










        else:
            return HttpResponse(json.dumps({'no': 'no'}), content_type='application/json')

    except Exception as e:
        return HttpResponse(Exception(e), status=400)




def user_login(request):
    phone = request.POST.get('phone')
    pwd = request.POST.get('password')

    if phone == '+7(904)033-19-87':
        phone = 'admin'

    if phone and pwd:
        user = authenticate(username=phone, password=pwd)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home.html')

    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')

def home_view(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')




@login_required
def orders_view(request):
    name = request.POST.get('ordername')
    comment = request.POST.get('ordercomment')
    if name:
        order_obj = Order(name=name, comment=comment, created_at=datetime.now())
        order_obj.save()
        price_obj = Price(order_id_id=order_obj.id)
        price_obj.save()

    order_obj = Order.objects.all().order_by('-id')

    return render(request, 'orders/orders.html', {'orders': order_obj})


@login_required
def orderinfo_view(request, orderid):
    from django.db.models import Sum


    order_m = Order.objects.filter(id=orderid).values()[0]
    price_m = Price.objects.filter(order_id=orderid).values()

    # if cupboardid and cupboardcount in request then created Cupboard model
    cupboardid = request.POST.get('cupboardid')
    cupboardcount = request.POST.get('cupboardcount')
    if id and cupboardcount:
        cupboard_m = Cupboard(count=cupboardcount, base_id_id=cupboardid, price_id_id=price_m[0]['id'])
        cupboard_m.save()
    else:
        cupboard_m = None


    if price_m:
        cupboard_m = Cupboard.objects.filter(price_id=price_m.values('id')[0]['id'])
        count_tabletop = 0
        count_loop = 0
        count_handle = 0
        count_hitch = 0
        count_baguette = 0
        count_roof = 0
        count_facade = 0
        count_facadeskin = 0
        count_facadeskingl = 0
        count_facadeplastic = 0
        for coupboard in cupboard_m:
            count_tabletop += coupboard.count * coupboard.base_id.tabletop
            count_loop += coupboard.count * coupboard.base_id.loop
            count_handle += coupboard.count * coupboard.base_id.handle
            count_hitch += coupboard.count * coupboard.base_id.hitch
            count_baguette += coupboard.count * coupboard.base_id.baguette
            count_roof += coupboard.count * coupboard.base_id.roof
            count_facade += coupboard.count * coupboard.base_id.facade
            count_facadeskin += coupboard.count * coupboard.base_id.skin
            count_facadeskingl += coupboard.count * coupboard.base_id.skingl
            count_facadeplastic += coupboard.count * coupboard.base_id.plastic

        for price in price_m:
            # counttabletop = cupboardlst.aggregate(Sum('count'))['count__sum'] * \
            #                 cupboardlst.aggregate(Sum('base_id__tabletop'))['base_id__tabletop__sum']
            price["tabletop"] = count_tabletop * 0.001
            price["loop"] = count_loop
            price["handle"] = count_handle
            price["hitch"] = count_hitch
            price["baguette"] = count_baguette * 0.001
            price["roof"] = count_roof
            price["facade"] = count_facade
            price["facadeskin"] = count_facadeskin * 0.001
            price["facadeskingl"] = count_facadeskingl * 0.001
            price["facadeplastic"] = count_facadeplastic * 0.001


    tabletop_price = Cost.objects.filter(costgroup_id=1)
    tabletopend_price = Cost.objects.filter(costgroup_id=2)
    tabletopedge_price = Cost.objects.filter(costgroup_id=3)
    plinth_price = Cost.objects.filter(costgroup_id=4)
    plinthcap_price = Cost.objects.filter(costgroup_id=5)
    wallpanel_price = Cost.objects.filter(costgroup_id=6)
    wallcap_price = Cost.objects.filter(costgroup_id=7)
    loop_price = Cost.objects.filter(costgroup_id=8)
    handle_price = Cost.objects.filter(costgroup_id=9)
    hitch_price = Cost.objects.filter(costgroup_id=10)
    rail_price = Cost.objects.filter(costgroup_id=11)
    baguette_price = Cost.objects.filter(costgroup_id=12)
    roof_price = Cost.objects.filter(costgroup_id=13)
    baluster_price = Cost.objects.filter(costgroup_id=14)
    socle_price = Cost.objects.filter(costgroup_id=15)
    drying_price = Cost.objects.filter(costgroup_id=16)
    backlight_price = Cost.objects.filter(costgroup_id=17)
    facade_price = Cost.objects.filter(costgroup_id=18)
    facadeskin_price = Cost.objects.filter(costgroup_id=19)
    facadeskingl_price = Cost.objects.filter(costgroup_id=20)
    facadeplastic_price = Cost.objects.filter(costgroup_id=21)

    prices = dict(tabletop=tabletop_price, tabletopend=tabletopend_price, tabletopedge=tabletopedge_price,
                  plinth=plinth_price, plinthcap=plinthcap_price, wallpanel=wallpanel_price,
                  wallcap=wallcap_price, loop=loop_price, handle=handle_price,
                  hitch=hitch_price, rail=rail_price, baguette=baguette_price,
                  roof=roof_price, baluster=baluster_price, socle=socle_price,
                  drying=drying_price, backlight=backlight_price, facade=facade_price,
                  facadeskin=facadeskin_price, facadeskingl=facadeskingl_price, facadeplastic=facadeplastic_price)

    return render(request, 'orders/info.html', {'order': order_m, 'cupboards': cupboard_m, 'price': price_m,
                                                'prices': prices})

@login_required
def prices_view(request):
    costgroup_m = CostGroup.objects.values()
    for costgroup in costgroup_m:
        costgroup['comment'] = Cost.objects.filter(costgroup_id=costgroup['id'])

    return render(request, 'prices/start.html', {'prices': costgroup_m})
