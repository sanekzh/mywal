from django.conf.urls import url
from django.views.generic import TemplateView

from landing import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^user_settings/$', views.user_settings, name='user_settings'),
    url(r'^list_of_products/$', views.user_products_list, name='list_of_products'),

]
