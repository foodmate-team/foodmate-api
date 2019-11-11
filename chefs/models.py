from django.db import models
from users.models import User

from functools import reduce
from statistics import median


class MenuItem(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Chef(User):
    user = models.OneToOneField(User, parent_link=True, on_delete=models.DO_NOTHING)
    subway = models.CharField(max_length=100, blank=True)
    ditance_from_subway = models.IntegerField()
    menu_items = models.ManyToManyField(MenuItem)
    address = models.CharField(max_length=200, blank=True)
    contact_fb = models.CharField(max_length=50, blank=True)
    contact_ok = models.CharField(max_length=50, blank=True)
    contact_inst = models.CharField(max_length=50, blank=True)
    contact_vk = models.CharField(max_length=50, blank=True)

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_median_price(self):
        prices = map(lambda m: m.price,
                     self.menu_items)

        return median(prices)



