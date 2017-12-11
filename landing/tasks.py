import requests

from mywal.celery import app

from .forms import Products
from .models import *


SUCCESS_RESPONSE = 200


@app.task
def auto_update_all_products():
    user_data_settings = Subscriber.objects.all()
    for user_setting in user_data_settings:
        apikey = user_setting.user_apikey
        name_user = Subscriber.objects.get(name=user_setting.name)
        print(name_user, ' ',apikey)
        all_user_products = Products.objects.filter(owner=name_user)
        for product in all_user_products:
            # print(product.upc)
            r = requests.get('http://api.walmartlabs.com/v1/items',
                             params={'apiKey': apikey, 'upc': product.upc})
            if r.status_code == SUCCESS_RESPONSE:
                upc = r.json().get('items').pop().get('upc')
                image_product = r.json().get('items').pop().get('mediumImage')
                title = r.json().get('items').pop().get('name')
                brand_name = r.json().get('items').pop().get('brandName')
                model = r.json().get('items').pop().get('modelNumber')
                in_stock = r.json().get('items').pop().get('stock')
                price = r.json().get('items').pop().get('salePrice')
                free_shipping = r.json().get('items').pop().get('freeShippingOver50Dollars')
                Products.objects.update_or_create(owner=name_user, upc=upc,
                                                  defaults={
                                                      'image_product': image_product,
                                                      'title': title,
                                                      'brand_name': brand_name,
                                                      'model': model,
                                                      'in_stock': in_stock,
                                                      'price': price,
                                                      'free_shipping': free_shipping,
                                                  })
                print('UPC: ', upc, ' updaiting... ok!')
    return print('ok!')

