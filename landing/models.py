from django.contrib.auth.models import User
from django.db import models


class Subscriber(models.Model):
    # session_key = models.CharField(max_length=128, blank=True, default='')
    name = models.CharField(max_length=128, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    user_apikey = models.CharField(max_length=128, blank=True, default='')
    # name = models.CharField(max_length=128, blank=True, null=True, default=None)
    # email = models.EmailField(blank=True, null=True, default=None)
    # user_apikey = models.CharField(max_length=128, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'subscribers'

    def __str__(self):
        return self.name


class Products(models.Model):
    owner = models.ForeignKey(Subscriber, blank=True, null=True, default=None)
    upc = models.CharField(max_length=12, blank=True)
    image_product = models.CharField(max_length=2053, blank=True)
    title = models.CharField(max_length=254, blank=True)
    brand_name = models.CharField(max_length=254, blank=True)
    model = models.CharField(max_length=254, blank=True)
    quantity = models.IntegerField(blank=True, default=0)
    in_stock = models.CharField(max_length=254, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    free_shipping = models.BooleanField(default=False)
    # last_product_change = models.CharField(max_length=128, default=None, null=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return "UPC:%s title:%s brand_name:%s" % (self.upc, self.title, self.brand_name)

