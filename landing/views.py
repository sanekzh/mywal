import requests

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpRequest
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .forms import UPC, SubscriberForm
from .models import *


SUCCESS_RESPONSE = 200


def user_settings(request):
    session_key = request.session.session_key
    user_data_settings = Subscriber.objects.filter(name=request.user.get_username())
    for user_setting in user_data_settings:
        email = user_setting.email
        user_apikey = user_setting.user_apikey
        context = {
            'email': email,
            'user_apikey': user_apikey
        }
    form = SubscriberForm(request.POST or None)
    if request.POST and form.is_valid():
        print('YES is_valid')
        data = form.cleaned_data
        print(data["name"])
        name = data['name']
        print(data["email"])
        email = data['email']
        print(data["user_apikey"])
        user_apikey = data['user_apikey']
        Subscriber.objects.update_or_create(name=name, defaults={'email': email, 'user_apikey': user_apikey})

    else:
        print("NO valid")

    return render(request, 'user_settings.html', locals())


def home(request):
    item = ''
    apikey = ''
    form = UPC(request.POST or None)
    if request.POST and form.is_valid():
        print('YES is_valid')
        data = form.cleaned_data
        print("UPC: ", data['upc'])
        upc = data['upc']
        user_data_settings = Subscriber.objects.filter(name=request.user.get_username())
        for user_setting in user_data_settings:
            email = user_setting.email
            apikey = user_setting.user_apikey
        r = requests.get('http://api.walmartlabs.com/v1/items',
                         params={'apiKey': apikey, 'upc': upc})
        # r = requests.get('http://api.walmartlabs.com/v1/items',
        #                  params={'apiKey': '5tkgtq74ffgptjd884pmuj8t', 'upc': upc})
        if r.status_code == SUCCESS_RESPONSE:
            # print(r.json().get('items').pop().get('name'))
            item = r.json().get('items').pop().get('name')
        else:
            print('Error! UPC not found')
            item = 'Error! UPC not found'
    else:
        print("NO valid")

    print(item)

    return render(request, 'home.html', locals())


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        print(self.user)
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")
