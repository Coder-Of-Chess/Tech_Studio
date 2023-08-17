from django.urls import path

from . import views
from .views import stripe_webhook_view

# app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog', views.blog, name='blog'),
    path('schedule', views.schedule, name='schedule'),
    path('partners', views.partners, name='partners'),
    path('team', views.team, name='team'),
    path('signup', views.signup, name='signup'),
    path('contact', views.contact, name='contact'),
    path('flayers', views.flayers, name='flayers'),
    path('chess', views.chess, name='chess'),
    path('products', views.products, name='products'),
    path('b_detail', views.b_details, name='b_detail'),
    path('b_detail2', views.b_details2, name='b_detail2'),
    path('productDetails/<int:id>/', views.product_detail, name='productDetails'),
    path('productForm', views.product_form, name='productForm'),
    path('payment', views.payment, name='payment'),
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session', views.create_checkout_session, name='create-checkout-session'),
    path('services-checkout-session', views.services_checkout_session, name='services-checkout-session'),
    path('stripe-webhook-paid', stripe_webhook_view),
    path('contact', stripe_webhook_view),

]
