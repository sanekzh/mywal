from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    pwd = models.CharField(max_length=128)

    def __str__(self):
        return "Name: %s            Email: %s" % (self.name, self.email)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'subscribers'