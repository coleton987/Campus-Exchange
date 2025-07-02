from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import random
import requests
import json


def register(request):
    if request.user.is_authenticated:
        return redirect('/')  # or wherever you want them to go
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            
            sent_code = random.randint(100000, 999999)
            request.session['sent_code'] = sent_code
            
            # Send verification email
            success = send_verification_email(form.cleaned_data['email'], sent_code)
            
            if success:
                messages.success(request, 'Verification code sent to your email!')
                return redirect(reverse('users:verification_form'))
            else:
                messages.error(request, 'Failed to send verification email. Please try again.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def send_verification_email(email, code):
    """Send verification email using Brevo Transactional Email API"""
    try:
        # Debug: Print the API key being used
        api_key = settings.EMAIL_API_KEY
        
        
        # Brevo API endpoint - Use the correct REST API URL
        url = "https://api.brevo.com/v3/smtp/email"
        
        # Try different header formats that Brevo might accept
        headers = {
            'api-key': api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Email payload
        payload = {
            "sender": {
                "name": "Campus Exchange",
                "email": settings.DEFAULT_FROM_EMAIL
            },
            "to": [
                {
                    "email": email,
                    "name": "User"
                }
            ],
            "templateId": 1,  # Your verification-code template ID
            "params": {
                "code": str(code)
            }
        }
        
        # Send the email
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        print(f"Brevo Response Status: {response.status_code}")
        print(f"Brevo Response Body: {response.text}")
        
        # Check if request was successful
        if response.status_code == 201:
            return True
        else:
            print(f"Brevo API Error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Brevo Email Error: {e}")
        return False


def verification_form(request):
    sent_code = request.session.get('sent_code')
    form_data = request.session.get('form_data')
    
    # Redirect to register if no session data
    if not sent_code or not form_data:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('users:register')
    
    print(f"Stored code: {sent_code}")
    
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        print(f"Entered code: {entered_code}")
        
        try:
            if int(entered_code) == sent_code:
                # Create the user
                form = CustomUserCreationForm(form_data)
                if form.is_valid():
                    user = form.save()
                    user.set_full_name(form_data.get('full_name'))
                    user.save()
                    
                    # Clear session data
                    del request.session['sent_code']
                    del request.session['form_data']
                    
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('/listing/products')
                else:
                    messages.error(request, 'There was an error creating your account.')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid 6-digit code.')
    
    return render(request, 'verification_form.html', {
        'email': form_data.get('email') if form_data else ''
    })


def resend_verification_code(request):
    """Handle resending verification code via AJAX"""
    if request.method == 'POST':
        form_data = request.session.get('form_data')
        
        if not form_data:
            return JsonResponse({
                'success': False, 
                'message': 'Session expired. Please register again.'
            })
        
        # Generate new code
        new_code = random.randint(100000, 999999)
        request.session['sent_code'] = new_code
        request.session.modified = True
        
        # Send new email
        email = form_data.get('email')
        success = send_verification_email(email, new_code)
        
        if success:
            return JsonResponse({
                'success': True,
                'message': 'New verification code sent to your email!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Failed to send verification email. Please try again.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def log_in(request):
    if request.user.is_authenticated:
        return redirect('/')  # or wherever you want them to go
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'log_in.html', {'num': 1})
    else:
        return render(request, 'log_in.html')


def log_out(request):
    logout(request)
    return redirect('/')