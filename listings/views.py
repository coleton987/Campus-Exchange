import json
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm  # Make sure you're importing the correct form
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
    my_listings = request.GET.get('my_listings', '')  # Check for my_listings parameter
    
    # Start with base queryset
    products = Product.objects.all()
    
    # Filter by current user's listings if requested
    if my_listings and request.user.is_authenticated:
        products = products.filter(seller=request.user)
    
    # Apply search query if provided
    if query:
        products = products.filter(
            name__icontains=query
        ) | products.filter(
            description__icontains=query
        )
        # If we're filtering by user AND searching, we need to combine the filters
        if my_listings and request.user.is_authenticated:
            products = products.filter(seller=request.user)
    
    # Prefetch ordered images to avoid N+1 queries
    products = products.prefetch_related('images')
    
    # Add context for template to know if we're showing user's listings
    context = {
        'products': products,
        'showing_my_listings': bool(my_listings and request.user.is_authenticated),
        'current_user': request.user if request.user.is_authenticated else None
    }
    
    return render(request, 'list.html', context)


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    # Images will be automatically ordered due to Meta ordering in model
    return render(request, 'product_detail.html', {'product': product})

def edit_listing(request, id):
    # Get the product first
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        # Use the existing product instance and update it with POST data
        edit_form = ProductForm(request.POST, instance=product)
        
        if edit_form.is_valid():
            # Save the updated product
            updated_product = edit_form.save()
            
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Product updated successfully',
                    'redirect_url': f'/listing/product_details/{updated_product.id}/'
                })
            else:
                return redirect('product_details', id=updated_product.id)
        else:
            # Form has errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': edit_form.errors
                }, status=400)
            else:
                return render(request, 'edit_listing.html', {
                    'form': edit_form, 
                    'product': product,
                    'errors': edit_form.errors
                })
    else:
        # GET request - create form with existing product data
        edit_form = ProductForm(instance=product)
    
    return render(request, 'edit_listing.html', {
        'form': edit_form, 
        'product': product
    })

def remove_image(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        image_id = data.get('image_id')
        
        if not image_id:
            return JsonResponse({'error': 'Image ID is missing'}, status=400)
        
        try:
            # Get the image and check if the user owns the product
            product_image = ProductImage.objects.get(id=image_id)
            
            # Optional: Add permission check
            # if product_image.product.seller != request.user:
            #     return JsonResponse({'error': 'Permission denied'}, status=403)
            
            # Delete the image
            product_image.delete()
            
            return JsonResponse({'message': 'Image removed successfully'}, status=200)
            
        except ProductImage.DoesNotExist:
            return JsonResponse({'error': 'Image not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)





def update_photo_order(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        order_changes = data.get('order_changes')
        
        # Get the product
        product = Product.objects.get(id=product_id, seller=request.user)
        
        # Update image orders
        for image_id, new_order in order_changes.items():
            try:
                image = product.images.get(id=image_id)
                image.order = new_order  # Assuming you have an 'order' field
                image.save()
            except:
                continue
                
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})