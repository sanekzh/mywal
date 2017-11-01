import requests
import simplejson as json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpRequest
from django.contrib.auth.models import User
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import serializers
from django.contrib.auth import login, logout

from .forms import UPC, SubscriberForm, Products
from .models import *


SUCCESS_RESPONSE = 200
ITEM = ''


def user_settings(request):
    context = []
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
        print(data['name'])
        name = data['name']
        print(data['email'])
        email = data['email']
        print(data['user_apikey'])
        user_apikey = data['user_apikey']
        Subscriber.objects.update_or_create(name=name, defaults={'email': email, 'user_apikey': user_apikey})
        user_data_settings = Subscriber.objects.filter(name=request.user.get_username())
    else:
        print("NO valid")

    return render(request, 'user_settings.html', locals())


def home(request):
    item = ''
    apikey = ''
    form = UPC(request.POST or None)
    if request.method == "POST" and form.is_valid():
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
            upc = r.json().get('items').pop().get('upc')
            image_product = r.json().get('items').pop().get('mediumImage')
            title = r.json().get('items').pop().get('name')
            brand_name = r.json().get('items').pop().get('brandName')
            model = r.json().get('items').pop().get('modelNumber')
            in_stock = r.json().get('items').pop().get('stock')
            price = r.json().get('items').pop().get('salePrice')
            free_shipping = r.json().get('items').pop().get('freeShippingOver50Dollars')
            name = Subscriber.objects.get(name=request.user.get_username())
            try:
                Products.objects.update_or_create(owner=name, upc=upc,
                                                  defaults={
                                                      'image_product': image_product,
                                                      'title': title,
                                                      'brand_name': brand_name,
                                                      'model': model,
                                                      'in_stock': in_stock,
                                                      'price': price,
                                                      'free_shipping': free_shipping,
                                                  })
            except ValueError:
                print('error!!!')
            global ITEM
            ITEM = title
        else:
            print('Error! UPC not found')
            item = 'Error! UPC not found'

    else:
        print("NO valid")
    print("Product name: ", item)
    context = {
        'item': ITEM,
    }

    return render(request, 'home.html', context)


def user_products_list(request):
    if request.method == 'GET':
        print('ajax')
        name = Subscriber.objects.get(name=request.user.get_username())
        queryset = Products.objects.filter(owner=name)
        json_data = serializers.serialize('json', queryset)
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')


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
