from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product, ProductImage
from django.http import JsonResponse


def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)

        if product_form.is_valid():
            product = product_form.save(commit=False)  # Don't save yet
            product.seller = request.user  # Set the seller to the currently logged-in user
            product.save()
            # Return the product ID as JSON response
            return JsonResponse({'product_id': product.id}, status=200)
        else:
            return JsonResponse({'errors': product_form.errors}, status=400)
    else:
        product_form = ProductForm()

    return render(request, 'add.html', {'product_form': product_form})


def file_upload(request):
    if request.method == 'POST':
        # Fetch the product (you may need to send product ID from Dropzone)
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'error': 'Product ID is missing'}, status=400)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        # Get the file from the request
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        # Get the current order for this image
        # This will be the next available order number (0-indexed)
        current_image_count = ProductImage.objects.filter(product=product).count()
        
        # Limit to 6 images
        if current_image_count >= 6:
            return JsonResponse({'error': 'Maximum 6 images allowed'}, status=400)
        
        # Create a ProductImage instance and associate it with the product
        product_image = ProductImage(
            product=product, 
            image=file,
            order=current_image_count  # Set order based on current count
        )
        product_image.save()

        # Respond with success or relevant data
        return JsonResponse({
            'message': 'Image uploaded successfully', 
            'image_id': product_image.id,
            'order': product_image.order
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def product_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            name__icontains=query
        ) | Product.objects.filter(
            description__icontains=query
        )
    else:
        products = Product.objects.all()
    
    # Prefetch ordered images to avoid N+1 queries
    products = products.prefetch_related('images')
    
    return render(request, 'list.html', {'products': products})


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    # Images will be automatically ordered due to Meta ordering in model
    return render(request, 'product_detail.html', {'product': product})