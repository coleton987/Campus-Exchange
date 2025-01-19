from django.shortcuts import render, redirect
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def start_onboarding(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = request.user

        try:
            # Create a Stripe Connect account
            account = stripe.Account.create(
                type="express",  # Use "express" for Stripe-hosted onboarding
                country="US",
                email=user.email,
                business_profile={
                    "name": f"{user.full_name} Campus Exchange Seller",
                    "url": f"https://coleton987-1.loca.lt/seller/register_seller/",
                },
                capabilities={
                    "card_payments": {"requested": True},
                    "transfers": {"requested": True},
                },
            )

            # Save the account ID for future reference
            # (Assumes you have a Seller model linked to your user)
            # seller = Seller.objects.create(user=request.user, stripe_account_id=account.id)

            # Generate an Account Link
            account_link = stripe.AccountLink.create(
                account=account.id,
                refresh_url="https://coleton987-1.loca.lt/seller/register_seller/",
                return_url="https://coleton987-1.loca.lt/seller/register_seller/",
                type="account_onboarding",
                collection_options={"fields": "eventually_due"},
                
            )

            

            # Redirect the seller to the onboarding link
            return redirect(account_link.url)

        except stripe.error.StripeError as e:
            return render(request, "error.html", {"error": str(e)})

    return render(request, "register_seller.html")
