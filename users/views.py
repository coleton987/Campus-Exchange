from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from django.urls import reverse
import random
from home import settings
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            
            sent_code = random.randint(100000, 999999)
            request.session['sent_code'] = sent_code
            messages = Mail(
                from_email='cmill026@students.bju.edu',
                to_emails=form.cleaned_data['email'],
                subject='Campus Exchange Message',
                html_content=f'<strong>{sent_code}</strong>')
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(messages)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)
            return redirect(reverse('users:verification_form'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def verification_form(request):
    sent_code = request.session.get('sent_code')
    print(sent_code)
    if request.method == 'POST':
        print(request.POST.get('code'))
        if int(request.POST.get('code')) == sent_code:

            form = CustomUserCreationForm(request.session.get('form_data'))
            user = form.save()
            user.set_full_name(form.cleaned_data.get('full_name')) 
            login(request, user)
            return redirect('/listing/products')  # Redirect to the products listing page after successful registration

    return render(request, 'verification_form.html')



def log_in(request):
    
    if request.method == "POST":
        username = request.POST.get('username')  # Use .get() instead of ['username']
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            x={ 'num': 1}
            return render(request, 'log_in.html', x)
    else:
        return render(request, 'log_in.html')
    
def log_out(request):
    logout(request)
    return redirect('/')
    