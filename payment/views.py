from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import stripe
from listings.models import Product
from home import settings

# Stripe key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Render the payment form with Stripe's Payment Intent
def payment_form(request, product_id):
    # Get product details
    product = get_object_or_404(Product, id=product_id)

    # Create a PaymentIntent to generate a client_secret
    intent = stripe.PaymentIntent.create(
        amount=int(product.price) * 100,  # Amount in cents
        currency='usd',
        automatic_payment_methods={"enabled": False},
        payment_method_types=["card", "cashapp"],  
        
    )

    # Pass the product_id and client_secret to the frontend
    context = {
        'product_id': product_id,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'payment_form.html', context)


# Process the payment after form submission
def process_payment(request, product_id):
    
    if request.method == 'POST':
        # Get product details
        product = get_object_or_404(Product, id=product_id)

        # Retrieve the payment method ID from the form
        payment_method_id = request.POST.get('payment_method_id')
        client_secret = request.POST.get('client_secret')
        print(f"Payment Method ID: {request.POST.get('payment_method_id')}")
        print(f"Client Secret: {request.POST.get('client_secret')}")

        if not payment_method_id or not client_secret:
            return JsonResponse({'error': 'Payment method ID or client secret is missing'}, status=400)

        try:
            # Confirm the PaymentIntent with the payment method
            intent = stripe.PaymentIntent.confirm(
                client_secret,
                payment_method=payment_method_id,
                confirm=True,  # This ensures immediate confirmation
            )
            print("WOOO")
            # Check if the payment was successful
            if intent.status == 'succeeded':
                # Payment was successful, redirect to success page
                
                return redirect('payment_success', product_id=product_id)
            else:
                return JsonResponse({'error': 'Payment failed'}, status=400)

        except stripe.error.CardError as e:
            return JsonResponse({'error': f'Payment failed: {e.user_message}'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Payment success page
def payment_success(request, product_id):
    # You can add any success messages or logic here
    return render(request, 'payment_success.html', {'product_id': product_id})
