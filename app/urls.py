from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^.*/ajax/$', views.ajax_view, name='ajax'),

    url(r'^$', views.home_view, name='home'),
    url(r'^orders/$', views.orders_view, name='orders'),
    url(r'^orderinfo/(?P<orderid>\d+)/$', views.order_info_view, name='order_info'),

]

