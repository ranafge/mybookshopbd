from django import template
# from core.models import Order

from .. import models

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = models.Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].books.count()
    return 0


@register.simple_tag()
def multiply(qty, unit_price,  *args, **kwargs):
    return qty * unit_price



















