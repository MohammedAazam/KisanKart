from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def ai_price(request):
    return render(request, 'ai_price.html')


def products(request):
    return render(request, 'product.html')

def profile(request):
    return render(request, 'profile.html')
