from django.shortcuts import render, redirect
from django.contrib import messages
from user.forms import RegistrationForm,SignInForm
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'auth/register.html')
            user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            )
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}!')
            return redirect('/')
        else:
            messages.error(request,form.errors)
    return render(request,"auth/register.html")


def signIn(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignInForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('/')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/sign_in.html')


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('sign_in')