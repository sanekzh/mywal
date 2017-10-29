from django.contrib.auth.models import User
from django.db import models


class Subscriber(models.Model):
    session_key = models.CharField(max_length=128, blank=True, default='')
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
        return "name:%s email:%s user_apikey:%s" % (self.name, self.email, self.user_apikey)


class Products(models.Model):
    user = models.ForeignKey(Subscriber, blank=True, null=True, default=None) #on_delete=models.CASCADE)
    upc = models.CharField(max_length=24)
    image_product = models.CharField(max_length=24)
    title = models.CharField(max_length=128, default=None, null=True)
    brand_name = models.CharField(max_length=128)
    model = models.EmailField(default=None)
    quantity = models.DateField(default=None, null=True)
    in_stock = models.CharField(max_length=128, default=None, null=True)
    price = models.CharField(max_length=128, default=None, null=True)
    free_shipping = models.CharField(max_length=128, default=None, null=True)
    last_product_change = models.CharField(max_length=128, default=None, null=True)
