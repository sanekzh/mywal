import requests

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from .forms import UPC, SubscriberForm
from .models import *


SUCCESS_RESPONSE = 200


def user_settings(request):
    form = SubscriberForm(request.POST or None)
    if request.POST and form.is_valid():
        print('YES is_valid')
        data = form.cleaned_data
        print(data["name"])
        print(data["email"])
        print(data["user_apikey"])
        new_form = form.save()
    else:
        print("NO valid")
    items = Subscriber.objects.all()
    for item in items:
        email = item.email
        user_apikey = item.user_apikey
    return render(request, 'user_settings.html', locals())


def home(request):
    item = ''
    form = UPC(request.POST or None)
    if request.POST and form.is_valid():
        print('YES is_valid')
        data = form.cleaned_data
        print("UPC: ", data['upc'])
        upc = data['upc']
        apikey = SubscriberForm.user_apikey
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
        # SubscriberForm.name = User.username
        # SubscriberForm.email = ""
        print("test1 = ", )
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
