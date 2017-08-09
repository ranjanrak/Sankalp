from django.conf.urls import url
from . import views
app_name = 'daychangers'

urlpatterns = [
	url(r'^$',views.login_user, name='login_user'),
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$',views.register, name='register'),     
    url(r'^data/$',views.data, name='data'),
    url(r'^checkorder/$',views.checkorder, name='checkorder'),
    url(r'^addsymbol/$',views.addsymbol, name='addsymbol'),
    url(r'^holding/$',views.holding, name='holding'),
    url(r'^login/$',views.login_user, name='login_user'),
    url(r'^orders/$',views.orders, name='orders'),
    url(r'^logout/$',views.logout_user, name='logout_user'),
]
