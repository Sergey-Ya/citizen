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

from .models import Order, Price, Cupboard, CupboardLst, CostGroup, Cost

from datetime import datetime
import json

from app.magic import base



def ajax_view(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action')
            rp = request.POST


            if action == 'send_sms':
                base.send_sms(rp.get('phone'))
                return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')


            if action == 'add_order':
                now = datetime.now()
                order_m = Order(name=rp.get('name'), comment=rp.get('comment'), created_at=now)
                order_m.save()
                price_m = Price(order_id_id=order_m.id)
                price_m.save()
                now = dateformat.format(now, settings.DATE_FORMAT)
                return HttpResponse(json.dumps({'status': 'ok', 'id': order_m.id, 'createdat': now}), content_type='application/json')

            if action == 'del_order':
                Order.objects.filter(id=rp.get('id')).delete()
                return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')
            if action == 'edit_order':
                Order.objects.filter(id=rp.get('id')).update(name=rp.get('name'), comment=rp.get('comment'))
                return HttpResponse(json.dumps({'status': 'ok'}), content_type='application/json')




            if action == 'save_price':
                id = rp.get('priceid')
                data = json.loads(rp.get('data'))
                data2 = json.loads(rp.get('data2'))

                print(data2)

                Price.objects.filter(id=id).update(tabletopend=data['tabletopend'], tabletopedge=data['tabletopedge'],
                                                   plinth=data['plinth'], plinthcap=data['plinthcap'],
                                                   wallpanel=data['wallpanel'], wallcap=data['wallcap'],
                                                   rail=data['rail'], baluster=data['baluster'],
                                                   socle=data['socle'], drying=data['drying'],
                                                   backlight=data['backlight'],

                                                   tabletop_cost_id_id=data2['tabletop_cost'],
                                                   tabletopend_cost_id_id=data2['tabletopend_cost'],
                                                   tabletopedge_cost_id_id=data2['tabletopedge_cost'],
                                                   plinth_cost_id_id=data2['plinth_cost'],
                                                   plinthcap_cost_id_id=data2['plinthcap_cost'],
                                                   wallpanel_cost_id_id=data2['wallpanel_cost'],
                                                   wallcap_cost_id_id=data2['wallcap_cost'],
                                                   loop_cost_id_id=data2['loop_cost'],
                                                   handle_cost_id_id=data2['handle_cost'],
                                                   hitch_cost_id_id=data2['hitch_cost'],
                                                   rail_cost_id_id=data2['rail_cost'],
                                                   baguette_cost_id_id=data2['baguette_cost'],
                                                   roof_cost_id_id=data2['roof_cost'],
                                                   baluster_cost_id_id=data2['baluster_cost'],
                                                   socle_cost_id_id=data2['socle_cost'],
                                                   drying_cost_id_id=data2['drying_cost'],
                                                   backlight_cost_id_id=data2['backlight_cost'],
                                                   facade_cost_id_id=data2['facade_cost'],
                                                   facadeskin_cost_id_id=data2['facadeskin_cost'],
                                                   facadeskingl_cost_id_id=data2['facadeskingl_cost'],
                                                   facadeplastic_cost_id_id=data2['facadeplastic_cost'],
                                                   othercost=rp.get('othercost'),
                                                   facadeskintype=rp.get('facadeskintype'))

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
        phone = 'sergey'

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

    return render(request, 'orders/start.html', {'orders': order_obj})

@login_required
def orderinfo_view(request, orderid):
    from django.db.models import Sum


    order_m = Order.objects.filter(id=orderid).values()[0]
    price_m = Price.objects.filter(order_id=orderid).values()

    # if cupboardid and cupboardcount in request then created Cupboard model
    action = request.POST.get('action')
    cupboardlstid = request.POST.get('cupboardlstid')
    cupboardcount = request.POST.get('cupboardcount')

    cupboardid = request.POST.get('cupboardid')


    if action == 'add' and cupboardlstid and cupboardcount:
        cupboardprice_m = Cupboard(price_id_id=price_m[0]['id'], cupboardlst_id_id=cupboardlstid, count=cupboardcount)
        cupboardprice_m.save()
    elif action == 'edit' and cupboardid and cupboardlstid and cupboardcount:
        Cupboard.objects.filter(id=cupboardid).update(cupboardlst_id_id=cupboardlstid, count=cupboardcount)
    elif action == 'del' and cupboardid:
        Cupboard.objects.filter(id=cupboardid).delete()



    cupboard_m = Cupboard.objects.filter(price_id=price_m.values('id')[0]['id'])

    tabletop_cnt = 0
    loop_cnt = 0
    handle_cnt = 0
    hitch_cnt = 0
    baguette_cnt = 0
    roof_cnt = 0
    facade_cnt = 0
    facadeskin_cnt = 0
    facadeskingl_cnt = 0
    facadeplastic_cnt = 0

    for cupboard in cupboard_m:
        tabletop_cnt += cupboard.count * cupboard.cupboardlst_id.tabletop
        loop_cnt += cupboard.count * cupboard.cupboardlst_id.loop
        handle_cnt += cupboard.count * cupboard.cupboardlst_id.handle
        hitch_cnt += cupboard.count * cupboard.cupboardlst_id.hitch
        baguette_cnt += cupboard.count * cupboard.cupboardlst_id.baguette
        roof_cnt += cupboard.count * cupboard.cupboardlst_id.roof
        facade_cnt += cupboard.count * cupboard.cupboardlst_id.facade
        facadeskin_cnt += cupboard.count * cupboard.cupboardlst_id.skin
        facadeskingl_cnt += cupboard.count * cupboard.cupboardlst_id.skingl
        facadeplastic_cnt += cupboard.count * cupboard.cupboardlst_id.plastic

    for price in price_m:
        price["tabletop"] = tabletop_cnt * 0.001
        price["loop"] = loop_cnt
        price["handle"] = handle_cnt
        price["hitch"] = hitch_cnt
        price["baguette"] = baguette_cnt * 0.001
        price["roof"] = roof_cnt
        price["facade"] = facade_cnt
        price["facadeskin"] = facadeskin_cnt * 0.001
        price["facadeskingl"] = facadeskingl_cnt * 0.001
        price["facadeplastic"] = facadeplastic_cnt * 0.001


    tabletop_cost = Cost.objects.filter(costgroup_id=1)
    tabletopend_cost = Cost.objects.filter(costgroup_id=2)
    tabletopedge_cost = Cost.objects.filter(costgroup_id=3)
    plinth_cost = Cost.objects.filter(costgroup_id=4)
    plinthcap_cost = Cost.objects.filter(costgroup_id=5)
    wallpanel_cost = Cost.objects.filter(costgroup_id=6)
    wallcap_cost = Cost.objects.filter(costgroup_id=7)
    loop_cost = Cost.objects.filter(costgroup_id=8)
    handle_cost = Cost.objects.filter(costgroup_id=9)
    hitch_cost = Cost.objects.filter(costgroup_id=10)
    rail_cost = Cost.objects.filter(costgroup_id=11)
    baguette_cost = Cost.objects.filter(costgroup_id=12)
    roof_cost = Cost.objects.filter(costgroup_id=13)
    baluster_cost = Cost.objects.filter(costgroup_id=14)
    socle_cost = Cost.objects.filter(costgroup_id=15)
    drying_cost = Cost.objects.filter(costgroup_id=16)
    backlight_cost = Cost.objects.filter(costgroup_id=17)
    facade_cost = Cost.objects.filter(costgroup_id=18)
    facadeskin_cost = Cost.objects.filter(costgroup_id=19)
    facadeskingl_cost = Cost.objects.filter(costgroup_id=20)
    facadeplastic_cost = Cost.objects.filter(costgroup_id=21)

    costs = dict(tabletop=tabletop_cost, tabletopend=tabletopend_cost, tabletopedge=tabletopedge_cost,
                 plinth=plinth_cost, plinthcap=plinthcap_cost, wallpanel=wallpanel_cost,
                 wallcap=wallcap_cost, loop=loop_cost, handle=handle_cost,
                 hitch=hitch_cost, rail=rail_cost, baguette=baguette_cost,
                 roof=roof_cost, baluster=baluster_cost, socle=socle_cost,
                 drying=drying_cost, backlight=backlight_cost, facade=facade_cost,
                 facadeskin=facadeskin_cost, facadeskingl=facadeskingl_cost, facadeplastic=facadeplastic_cost)

    cupboardlst_m = CupboardLst.objects.all()

    return render(request, 'order/start.html', {'order': order_m, 'price': price_m, 'cupboard': cupboard_m,
                                                'costs': costs, 'cupboardlst': cupboardlst_m})

@login_required
def prices_view(request):
    costgroup_m = CostGroup.objects.values()
    for costgroup in costgroup_m:
        costgroup['comment'] = Cost.objects.filter(costgroup_id=costgroup['id'])

    return render(request, 'prices/start.html', {'prices': costgroup_m})
