from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^.*/ajax/$', views.ajax_view, name='ajax'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^$', views.home_view, name='home'),

    url(r'^orders/$', views.orders_view, name='orders'),
    url(r'^orders/(?P<orderid>\d+)/$', views.orderinfo_view, name='orderinfo'),

    url(r'^prices/$', views.prices_view, name='prices'),

]

