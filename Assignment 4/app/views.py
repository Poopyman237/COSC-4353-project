from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

from app.forms import ProfileForm, FuelQuoteForm
from app.models import FuelQuote


def home(request):
    return render(request, 'app/home.html')


def register(request):
    context = {}
    # view generates our form with empty information or
    # the request.POST data if there is any.

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # form.is_valid() verifies if the two passwords
        # are the same by calling validate_password() which then calls
        # set_password() to hash and save our password
        if form.is_valid():
            form.save()
            return redirect('app:login')
    else:
        form = UserCreationForm()
    context['form'] = form
    return render(request, 'app/register.html', context)


def login_view(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('app:edit_profile')

        return render(request, 'app/login.html', {'form': form})

    else:
        form = AuthenticationForm()

        return render(request, 'app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('app:home')


def profile(request):
    return render(request, 'app/profile.html')


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('app:profile')
    context = {
        'form': form
    }
    print(form.errors)

    return render(request, 'app/edit_profile.html', context)



@login_required
def fuel_quote(request):

    if request.method == 'POST':
        form = FuelQuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:fuel_history')
    else:
        form = FuelQuoteForm(initial={
            'delivery_address': request.user.profile.address_1,
        })
    context = {
        'form': form
    }

    return render(request, 'app/fuelform.html', context)


def fuel_history(request):
    context = {
        'quotes': FuelQuote.objects.all(),
    }
    return render(request, 'app/FuelQuoteHistory.html', context)
