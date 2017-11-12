import requests
import csv

from django.shortcuts import render
from datetime import date
from django.utils.encoding import smart_str
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core import serializers
from django.contrib.auth import login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from .forms import UPC, SubscriberForm, Products
from .models import *


SUCCESS_RESPONSE = 200


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = reverse_lazy('mywal:login')
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy('mywal:index')

    def form_valid(self, form):
        self.user = form.get_user()
        print(self.user)
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('mywal:index'))


def home(request):
    return render(request, 'home.html')


def user_settings(request):
    context = []
    session_key = request.session.session_key
    # user_data_settings = Subscriber.objects.filter(name=request.user.get_username())
    # for user_setting in user_data_settings:
    #     email = user_setting.email
    #     user_apikey = user_setting.user_apikey
    #     context = {
    #         'email': email,
    #         'user_apikey': user_apikey
    #     }
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
        # user_data_settings = Subscriber.objects.filter(name=request.user.get_username())
    else:
        print("NO valid")

    user_data_settings = Subscriber.objects.filter(name=request.user.get_username())
    for user_setting in user_data_settings:
        email = user_setting.email
        user_apikey = user_setting.user_apikey
        context = {
            'email': email,
            'user_apikey': user_apikey
        }
    return render(request, 'user_settings.html', locals())


def upc_request(request):
    apikey = ''
    context = dict()
    context["description"] = '1234567'
    form = UPC(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print('YES is_valid')
        data = form.cleaned_data
        print("UPC: ", data['upc'])
        upc = data['upc']
        if upc != '':
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
                print(title)
                brand_name = r.json().get('items').pop().get('brandName')
                model = r.json().get('items').pop().get('modelNumber')
                in_stock = r.json().get('items').pop().get('stock')
                price = r.json().get('items').pop().get('salePrice')
                free_shipping = r.json().get('items').pop().get('freeShippingOver50Dollars')
                name = Subscriber.objects.get(name=request.user.get_username())
                # try:
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
                context["description"] = "yes"

            else:
                print('Error! UPC not found')
                context["description"] = "no"

        else:
            context["description"] = "no"

    else:
        print("NO valid")
        context["description"] = "no"
    print(context)
    return JsonResponse(context)


def user_products_list(request):
    if request.method == 'GET':
        print('start ajax request')
        name = Subscriber.objects.get(name=request.user.get_username())
        queryset = Products.objects.filter(owner=name)
        json_data = serializers.serialize('json', queryset)
        return HttpResponse(json_data, content_type='application/json')


def delete_product(request, product_id):
    try:
        queryset = Products.objects.filter(id=product_id).delete()
        print(queryset)
        print("pk = ", product_id)
    except ObjectDoesNotExist:
        print("Object Does Not Exist")

    return HttpResponseRedirect(reverse('mywal:home'))


def export_in_csv(request):
    name = Subscriber.objects.get(name=request.user.get_username())
    queryset = Products.objects.filter(owner=name)
    csvfile = 'products_list_{}_{}.csv'.format(name, date.today())
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(csvfile)
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"UPC"),
        smart_str(u"Link_Image"),
        smart_str(u"title"),
        smart_str(u"brand_name"),
        smart_str(u"model"),
        smart_str(u"price"),
        smart_str(u"quantity"),
        smart_str(u"in_stock"),
        smart_str(u"free_shipping"),
        smart_str(u"created"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.owner),
            smart_str(obj.upc),
            smart_str(obj.image_product),
            smart_str(obj.title),
            smart_str(obj.brand_name),
            smart_str(obj.model),
            smart_str(obj.price),
            smart_str(obj.quantity),
            smart_str(obj.in_stock),
            smart_str(obj.free_shipping),
            smart_str(obj.created),
        ])
    return response


def import_from_csv(request):
    if request.method == 'POST':

        csv_file = request.FILES['input_file']
        print(csv_file)
        csv_data = open(csv_file, mode='r')

    return request

