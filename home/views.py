from django.shortcuts import redirect, render
from django.http import HttpResponse

def healthz(request):
    return HttpResponse("OK")

def homepage(request):
        
    
    return render(request, 'home.html')

def about(request):
    if request.user.is_authenticated:
        return redirect('/')  # or wherever you want them to go
    return render(request, 'about.html')