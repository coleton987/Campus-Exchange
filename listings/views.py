from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product, ProductImage
from django.http import JsonResponse


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



def file_upload(request):
    for i in range(20):
        print("Hello")
    if request.method == 'POST':
        # Fetch the product (you may need to send product ID from Dropzone)
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'Product ID is missing'}, status=400)
        product = Product.objects.get(id=product_id)
        
        # Get the file from the request
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        # Create a ProductImage instance and associate it with the product
        product_image = ProductImage(product=product, image=file)
        product_image.save()

        # Respond with success or relevant data
        return JsonResponse({'message': 'Image uploaded successfully', 'image_id': product_image.id})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def product_list(request):
    products = Product.objects.all()
    product_images = ProductImage.objects.all()
    return render(request, 'list.html', {'products': products, 'product_images': product_images})


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


