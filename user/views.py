from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
def login_view(request):
    if request.method == "POST":        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.warning(request, 'Erro no login')      
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            login(request, user)
            return redirect('/')            
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, template_name='../templates/registration/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('/login') 