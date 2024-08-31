from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/about/')  # Redirect to the home page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


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
    