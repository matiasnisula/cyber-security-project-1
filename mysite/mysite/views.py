from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SecurityRiskSignupForm
from django.contrib.auth.models import User

# Safe sign up func below
#def signup(request):
#    if request.method == 'POST':
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password1')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('/login')
#    else:
#        form = UserCreationForm()
#    return render(request, 'registration/signup.html', {'form': form})

#Broken authentication
def signup(request):
    if request.method == 'POST':
        form = SecurityRiskSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            raw_password_confirm = form.cleaned_data.get('password_confirm')
            if (raw_password and raw_password_confirm and raw_password == raw_password_confirm):
                user = User.objects.create_user(username=username, password=raw_password)
                login(request, user)
                return redirect('/login')
            else:
                return render(request, 'registration/signup.html', {'form': form, "error": "error password missmatch"})
    else:
        form = SecurityRiskSignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def index(request):
    return render(request, "index.html")