import pickle
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .forms import ProductForm
from .models import Product

def home(request):
    return render(request, 'home.html', {'products': Product.objects.all()})

def ai_price(request):
    products = Product.objects.all()
    return render(request, 'ai_price.html', {'products': products})


def product_list(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    products = Product.objects.all()  # Default to all products

    if query:
        # Filter products by name or description (adjust as needed)
        products = products.filter(title__icontains=query)  # case-insensitive search for 'title'

    return render(request, 'product.html', {'products': products, 'query': query})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user 
            product.save()
            return redirect('products')  # Redirect after successful submission
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'edit_product.html', {'form': form, 'product': product,})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products')  # Redirect to the product list page

    # If it's a GET request, you can render a confirmation page
    return render(request, 'product_confirm_delete.html', {'product': product})


def profile(request):
    return render(request, 'profile.html')

# Load the pre-trained model (ensure the path is correct)
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)
    
def predict_price(request):
    suggestion = None

    if request.method == 'GET':
        farmprice = request.GET.get('farmprice')
        spread = request.GET.get('spread')

        if farmprice and spread:
            try:
                # Convert inputs to float for model prediction
                farmprice = float(farmprice)
                spread = float(spread)

                # Make the prediction using the pre-trained model
                suggestion = model.predict([[farmprice, spread]])[0]  # Assuming the model expects two inputs

            except Exception as e:
                suggestion = f"Error: {e}"

    return render(request, 'ai_price.html', {'suggestion': suggestion})


