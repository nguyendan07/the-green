from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

CATEGORY_CHOICES = (
    ('V', 'Vegetables'),
    ('F', 'Fruits'),
    ('J', 'Juice'),
    ('D', 'Dried')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.IntegerField("Discount (%)", blank=True, null=True)
    discount_price = models.FloatField("Price after discount", blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=1)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse("core:product-detail", kwargs=kwargs)

    def get_add_to_cart_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse("core:add-to-cart", kwargs=kwargs)

    def get_remove_from_cart_url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse("core:remove-from-cart", kwargs=kwargs)

    def save(self, *args, **kwargs):
        if self.discount:
            self.discount_price = self.price * (1 - self.discount / 100)
        if not self.slug:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} or {}".format(self.quantity, self.item.title)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        if self.item.discount_price:
            return self.quantity * self.item.discount_price
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total

    def get_total(self):
        total_discount = 0
        for order_item in self.items.all():
            total_discount += order_item.get_total_discount_item_price()
        return total_discount

    def get_total_amount_saved(self):
        return self.get_sub_total() - self.get_total()
