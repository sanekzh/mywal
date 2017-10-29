from django.conf.urls import url
from django.views.generic import TemplateView

from landing import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^home/$', views.home, name='home'),
    url(r'^user_settings/$', views.user_settings, name='user_settings'),
    url(r'^get_context_data/$', views.get_context_data, name='get_context_data'),
]
