import uuid
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django_resized import ResizedImageField
# Create your models here.
from django.shortcuts import reverse
from slugger import AutoSlugField
from django.conf import settings


class AutoSlugModel(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title')


class Publication(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookshop:publisher-detail', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookshop:category-detail', args=[self.slug])


class Author(models.Model):
    name = models.CharField(max_length=120)
    photo = ResizedImageField(size=[170, 162], upload_to='images', null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    division = models.CharField(max_length=150, blank=True, null=True)
    district = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField()
    slug = models.SlugField(blank=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bookshop:author-detail', args=[self.slug])

    def get_books_count(self):
        return models.Bookstore.object.filter(author=self).count()


class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Bookstore(models.Model):
    title = models.CharField(max_length=150, help_text='বাঙলার জমিদার')
    category = models.ManyToManyField(Category, max_length=150, help_text='প্রবন্ধ, গবেষণা ও অন্যান্য')
    subcategory = models.CharField(max_length=150, blank=True, null=True, help_text='প্রবন্ধ')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    published_date = models.DateField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(blank=True, help_text='প্রবন্ধ-গবেষণা-অন্যান্য')
    photo = ResizedImageField(size=[178, 121], upload_to='images', null=True, blank=True)
    book_details = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField()
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_category(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('bookshop:book-slug', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('bookshop:add-to-cart',
                       kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse('bookshop:remove-from-cart',
                       kwargs={'slug': self.slug})


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Bookstore, on_delete=models.CASCADE)
    edition = models.CharField(max_length=120, blank=True, null=True)


class x(models.Model):
    p = ResizedImageField(size=[178, 121], upload_to='images', null=True, blank=True)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    book = models.ForeignKey(Bookstore, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.book.title}"

    def get_total_book_price(self):
        return self.quantity * self.book.price

    def get_total_discount_book_price(self):
        return self.quantity * self.book.discount_price

    def get_amount_saved(self):
        return self.get_total_book_price() - self.get_total_discount_book_price()

    def get_final_price(self):
        if self.book.discount_price:
            return self.get_total_discount_book_price()
        return self.get_total_book_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=10, blank=True, null=True)
    books = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.books.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    another_phone = models.CharField(max_length=150)
    division = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    total_amount = models.CharField(max_length=10)
    payment_option = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return 'Billing address  of ' + self.user.username

    class Meta:
        verbose_name_plural = 'Address'


class Coupon(models.Model):
    code = models.CharField(max_length=10)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    email = models.EmailField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"


class SubjectChoice(models.Model):
    choice_text = models.CharField(max_length=150)

    def __str__(self):
        return self.choice_text


class Contact(models.Model):
    name = models.CharField(max_length=50, null=True
                            )
    contact_choice_text = models.ForeignKey(SubjectChoice, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=100)
    text = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.email


class SearchChoices(models.Model):
    search_text = models.CharField(max_length=50)

    def __str__(self):
        return self.search_text
