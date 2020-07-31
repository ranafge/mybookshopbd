from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views import generic
from . import models
from . import forms
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import string, random
import pdb
from django.db.models import Count
from django.db.models import Q


def index(request):
    books = models.Bookstore.objects.all().order_by('price')
    all_author = models.Author.objects.all()
    all_publication = models.Publication.objects.all()
    all_category = models.Category.objects.all()
    paginator = Paginator(books,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'books': books, 'all_author': all_author, "all_publication": all_publication,
                                          "all_category": all_category,'page_obj': page_obj})


def allbook(request):
    books = models.Bookstore.objects.all().order_by('-published_date')
    authors = models.Author.objects.filter(slug=books).annotate(num_books=Count('id'))
    all_author = models.Author.objects.all()
    all_publication = models.Publication.objects.all()
    all_category = models.Category.objects.all()
    return render(request, 'allbook.html',
                  {'books': books, 'authors': authors, 'all_author': all_author, "all_publication": all_publication,
                   "all_category": all_category})


def create_ref_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class AuthorDetail(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 3
    template_name = 'other/single_page.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.Author.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['author'] = self.object
        return context

    def get_queryset(self):
        return self.object.bookstore_set.all()


class PublisherDetail(generic.detail.SingleObjectMixin, generic.ListView):
    paginate_by = 3
    template_name = 'publication/publication_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=models.Publication.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(PublisherDetail, self).get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.object.bookstore_set.all()


class BookListView(generic.ListView):
    model = models.Bookstore
    template_name = 'bookstore/book_list.html'

    # queryset = models.Bookstore.objects.all()
    # context_object_name = 'book_list'
    # paginate_by = 1

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['myorderitem'] = models.OrderItem.objects.all()
        # context['mypublisher'] = self.publication not work
        # context['myauthor'] = self.Author not work
        # context['myauthor'] = self.Category not work

        return context


# Book details pk view works
class BookDetailView(generic.View):
    model = models.Bookstore

    # slug_field = 'pk'

    # template_name = 'bookstore/book_details.html' # View a template_name lage na

    def get(self, request, *args, **kwargs):
        # book = get_object_or_404(models.Bookstore, pk=kwargs.get('pk')) # not work
        book = get_object_or_404(models.Bookstore, pk=kwargs['pk'])
        context = {"book": book}
        return context


class BookDetailSlugView(generic.DetailView):
    model = models.Bookstore
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'bookstore/book_details.html'


class CategoryDetail(generic.DetailView, MultipleObjectMixin):
    model = models.Category
    paginate_by = 3
    template_name = "category/category_detail.html"

    def get_context_data(self, **kwargs):
        print()
        print(self.object)
        print()
        object_list = models.Bookstore.objects.filter(category=self.object)

        context = super(CategoryDetail, self).get_context_data(object_list=object_list, **kwargs)

        return context


class MyPhoto(generic.ListView):
    model = models.x
    template_name = 'photo.html'


class OrderSummary(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        try:
            order = models.Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'other/order_summary.html', {'order': order})
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an order.')
            return redirect(reverse('bookshop:index'))
        # return render(self.request, 'other/order_summary.html', {'order': order})


@login_required
def add_to_cart(request, slug):
    book = get_object_or_404(models.Bookstore, slug=slug)
    order_item, created = models.OrderItem.objects.get_or_create(
        user=request.user,
        ordered=False,
        book=book
    )
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.books.filter(book__slug=book.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "The Item Quantity Was Updated")
            return redirect('bookshop:order-summary')
        else:
            order.books.add(order_item)
            messages.info(request, "This Item Was Added To Your Cart")
            return redirect('bookshop:order-summary')
    else:
        ordered_date = timezone.now()
        order = models.Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.books.add(order_item)
        messages.info(request, "This Item Was Added To Your Cart")
        return redirect('bookshop:order-summary')


def remove_from_cart(request, slug):
    book = get_object_or_404(models.Bookstore, slug=slug)
    print()
    print(book)
    order_qs = models.Order.objects.filter(
        user=request.user, ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        if order.books.filter(book__slug=book.slug).exists():
            order_item = models.OrderItem.objects.filter(
                book=book, user=request.user, ordered=False
            )[0]
            order.books.remove(order_item)
            order_item.delete()
            messages.info(request, "This Item Was Removed From Your Cart")
            return redirect('bookshop:order-summary')
        else:
            messages.info(request, 'This Item Was Removed From Your Cart')
            return redirect('bookshop:order-summary')
    else:
        messages.info(request, 'You do not have an active order.')
        return redirect('bookshop:order-summary')


@login_required
def remove_single_item_from_cart(request, slug):
    book = get_object_or_404(models.Bookstore, slug=slug)
    order_qs = models.Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.books.filter(book__slug=book.slug).exists():
            order_item = models.OrderItem.objects.filter(book=book, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.books.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect('bookshop:order-summary')
    else:
        messages(request, 'You do not have an active order.')
        return redirect('bookshop:order-summary')


@method_decorator(login_required, name='dispatch')
class CheckoutView(generic.View):
    def get(self, *args, **kwargs):
        try:
            order = models.Order.objects.get(user=self.request.user, ordered=False)
            form = forms.CheckoutForm()
            couponform = forms.CouponForm()
            return render(self.request, 'other/checkout.html',
                          {'form': form, 'order': order, 'couponform': couponform, 'DISPLAY_COUPON_FORM': True})
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have order .')
            return redirect(reverse('bookshop:order-summary'))

    def post(self, *args, **kwargs):
        form = forms.CheckoutForm(self.request.POST or None)
        try:
            order = models.Order.objects.get(user=self.request.user, ordered=False)
            total_amount = order.get_total()

            if form.is_valid():
                full_name = form.cleaned_data.get("full_name")
                email = form.cleaned_data.get("email")
                phone = form.cleaned_data.get("phone")
                another_phone = form.cleaned_data.get("another_phone")
                division = form.cleaned_data.get("division")
                address = form.cleaned_data.get("address")
                payment_option = form.cleaned_data.get("payment_option")
                billing_address = models.BillingAddress(
                    user=self.request.user,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    another_phone=another_phone,
                    division=division,
                    address=address,
                    payment_option=payment_option,
                    total_amount=total_amount
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                order.ref_code = create_ref_code()
                order.save()
                order_items = order.books.all()
                order_items.update(ordered=True)
                for book in order_items:
                    book.save()
                order.ordered = True
                order.save()
                if payment_option == "C":
                    messages.info(self.request, 'Thanks for your order.')
                    return redirect('bookshop:thanks')
                elif payment_option == "RCT":
                    messages.info(self.request, 'This service not available yet. Please choose cash on delivery')
                    return redirect(reverse('bookshop:checkout'))
                else:
                    messages.success(self.request, 'This service is not available yet.Please choose cash on delivery')
                    return redirect(reverse('bookshop:checkout'))
                messages.success(request, 'Successfully submit your address. Please go to order confirm.')
                return redirect(reverse('bookshop:thanks'))
            else:
                messages.warning(self.request, 'Sorry, Its wrong coupon.')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an order.')
            return redirect(reverse('bookshop:index'))


class Thanks(generic.View):
    def get(self, *args, **kwargs):
        return render(self.request, 'other/payment.html')


def get_coupon(request, code):
    try:
        coupon = models.Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon does not exists.')
        return redirect(reverse('bookshop:checkout'))


class AddCouponView(generic.View):
    def post(self, *args, **kwargs):
        form = forms.CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = models.Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'Successfully added coupon.')
                return redirect(reverse('bookshop:checkout'))
            except ObjectDoesNotExist:
                messages.info(self.request, 'Not added coupon. You do not have an order.')
                return redirect(reverse('bookshop:checkout'))


class RequestRefund(generic.View):
    def get(self, *args, **kwargs):
        form = forms.RefundForm()
        return render(self.request, 'request_refund.html', {"form": form})

    def post(self, *args, **kwargs):
        form = forms.RefundForm(self.request.POST or None)
        if form.is_valid():
            ref_code = form.cleaned_data.get("ref_code")
            message = form.cleaned_data.get("message")
            email = form.cleaned_data.get("email")
            try:
                order = models.Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()
                refund = models.Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()
                messages.info(self.request, 'Your Refund request is received.')
                return redirect(reverse('bookshop:request-refund'))

            except ObjectDoesNotExist:
                messages.info(self.request, 'Order does not exits.')
                return redirect(reverse('bookshop:request-refund'))


def contact_us(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            contact = models.Contact()
            contact.contact_choice_text = form.cleaned_data.get("contact_choice_text")
            contact.phone_number = form.cleaned_data.get("phone_number")
            contact.email = form.cleaned_data.get("email")
            contact.text = form.cleaned_data.get("text")
            contact.name = form.cleaned_data.get("name")
            contact.save()
            send_mail("Contact from web subject", contact.text + ' ' + contact.phone_number + '' + contact.name,
                      contact.email, ['ranafge@gmail.com', 'samsul71bd@gmail.com'], fail_silently=True)
            messages.info(request, 'Thank for your message. We shall contact you soon.')
            return redirect(reverse('bookshop:index'))
        else:
            messages.warning(request, 'Please check the form again')
            return redirect(reverse('bookshop:contact-us'))
    else:
        form = forms.ContactForm()
    return render(request, 'contact_form.html', {'form': form})


def search(request):
    search_book_list = models.Bookstore.objects.all()
    query = request.GET.get("query")
    print(query)
    if query:
        search_book_list = models.Bookstore.objects.filter(
            Q(slug__icontains=query) |
            Q(title__icontains=query) |
            Q(author__name__icontains=query) |
            Q(author__slug__icontains=query) |
            Q(category__name__icontains=query) |
            Q(category__slug__icontains=query) |
            Q(publication__name__icontains=query) |
            Q(publication__slug__icontains=query) |
            Q(subcategory__icontains=query) |
            Q(price__icontains=query) |
            Q(discount_price__icontains=query) |
            Q(isbn__icontains=query) |
            Q(language__name__icontains=query)
        )

        paginator = Paginator(search_book_list, 3)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {
            "page_obj": posts,
            'query': query
        }

        return render(request, 'search.html', context)


class MySearchModel(generic.ListView):
    model = models.Bookstore
    context_object_name = 'objects'
    template_name = 'search.html'

    def get_queryset(self):
        qs = self.model.objects.all()
        search = self.request.GET.get('query')
        if search:
            qs = qs.filter(title__icontains=search)
            qs = qs.order_by('price')
        return qs


def all_author(request):
    all_author = models.Author.objects.all()
    return render(request, 'all_author.html', {'all_author': all_author})


def all_publication(request):
    all_publication = models.Publication.objects.all()
    return render(request, 'all_publication.html', {'all_publication': all_publication})


def all_category(request):
    all_category = models.Category.objects.all()
    return render(request, 'all_category.html', {'all_category': all_category})
