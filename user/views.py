from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from user.forms import RegistrationForm,SignInForm
from django.contrib.auth.decorators import login_required
from user.models import User, Address
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email'].lower()
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
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    return render(request,"auth/register.html")


def signIn(request):
    if request.user.is_authenticated:
        return redirect('index')


    form = SignInForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].lower()
        user = authenticate(
            request,
            username=email,
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
    return redirect('signIn')


@login_required
@require_POST
def add_address(request):
    phone_number = request.POST.get('phone_number', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    location = request.POST.get('location', '').strip()
    next_url = request.POST.get('next', '/')

    if not all([phone_number, city, state, location]):
        messages.error(request, 'All fields are required.')
        return redirect(next_url)

    is_default = not request.user.addresses.exists()
    Address.objects.create(
        user=request.user,
        phone_number=phone_number,
        city=city,
        state=state,
        location=location,
        is_default=is_default,
    )
    messages.success(request, 'Address added successfully.')
    return redirect(next_url)