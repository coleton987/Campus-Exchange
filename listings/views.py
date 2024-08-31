from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product, ProductImage
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404

def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)  # Handle file uploads with request.FILES
        images = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save()  # Save the form data to the model

            
            print(f"Number of images uploaded: {len(images)}")  # Debugging line
            for image in images:
                ProductImage(project=product, image=image).save()
                print(f"Processing image: {image.name}")  # Debugging line
            return redirect('product_list')  # Redirect to another page after saving
    else:
        form = ProductForm()
    
    return render(request, 'add.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    

    return render(request, 'list.html', {'products': products})

def product_details(request,id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})
