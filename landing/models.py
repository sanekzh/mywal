from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    email = models.EmailField(blank=True, null=True, default=None)
    user_apikey = models.CharField(max_length=128, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'subscribers'

    def __str__(self):
        return "Name: %s            Email: %s" % (self.name, self.email)
