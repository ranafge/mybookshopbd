from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from . import models

myModel = [models.Publication, models.Author, models.Category, models.Language,
           models.BookInstance, models.OrderItem,
           models.Coupon, models.Refund,  models.SubjectChoice,
           ]


def make_refund_accepted(queryset):
    queryset.update(refund_requested=True, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund'


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', "being_delivered", "received", "refund_requested", "refund_granted", 'coupon',
                    "billing_address"]
    list_display_links = ["user", "coupon", 'billing_address']
    list_filter = ["ordered", "being_delivered", "received", "refund_requested", "refund_granted"]
    search_fields = ['user__username', 'reference_code']
    actions = [make_refund_accepted]


@admin.register(models.Bookstore)
class BookAdmin(admin.ModelAdmin):
    model = models.Bookstore
    filter_horizontal = ('category',)
    list_display = ('title', 'author', "price_view", "publication", "discount_price", "isbn",)
    list_per_page = 10
    search_fields = ['title', 'author__name', 'publication__name', 'category__name']

    def price_view(self, obj):
        return obj.price

    price_view.empty_value_display = 'No know full_nameprice'


@admin.register(models.BillingAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user",'email', 'phone', "another_phone", "division", "address"]
    list_filter = ["user", "full_name", "email", "phone", "another_phone"]
    search_fields = ['user__username', 'full_name','phone', 'another_phone',"address"]


@admin.register(models.Contact)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name','contact_choice_text', 'phone_number', 'email','date','text',)
    search_fields = ('name','email', 'phone_number',)
    date_hierarchy = 'date'


admin.site.register(myModel)
