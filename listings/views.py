from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product, ProductImage

def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save()

            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return redirect('product_list')  # Redirect after saving
        else:
            print(product_form.errors)
    else:
        product_form = ProductForm()

    return render(request, 'add.html', {'product_form': product_form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'list.html', {'products': products})

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


