from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ai-price/', views.ai_price, name='ai_price'),
    path('products/', views.products, name='products'),
    path('profile/', views.profile, name='profile'),
]
