from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import re_path


app_name = 'bookshop'

urlpatterns = [
    path('', views.index, name='index'),
    path('allbook/', views.allbook, name='allbook'),
    path('publisher/<slug>/', views.PublisherDetail.as_view(), name='publisher-detail'),
    path('author/<slug>/', views.AuthorDetail.as_view(), name='author-detail'),
    path('book-list/', views.BookListView.as_view(), name='book-list'),
    path('book/<slug>/', views.BookDetailSlugView.as_view(), name='book-slug'),
    path('book/<pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('category/<slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('photo/', views.MyPhoto.as_view(), name='photo'),
    path('order-summary/', views.OrderSummary.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('thanks/', views.Thanks.as_view(), name='thanks'),
    path('add-coupon/', views.AddCouponView.as_view(), name='add-coupon'),
    path('request-refund/', views.RequestRefund.as_view(), name='request-refund'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('search/', views.search, name='search'),
    path('mysearch/', views.MySearchModel.as_view(), name='mysearch'),
    path('all-category/', views.all_category, name='all-category'),
    path('all-publication/', views.all_publication, name='all-publication'),
    path('all-author/', views.all_author, name='all-author'),

]
