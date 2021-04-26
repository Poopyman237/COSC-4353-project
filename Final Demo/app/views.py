from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

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


@login_required
def profile(request):
    return render(request, 'app/profile.html')


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('app:edit_profile')
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
            form_obj = form.save(commit=False)
            form_obj.user = request.user
            form_obj.save()
            return redirect('app:fuel_history')
    else:
        form = FuelQuoteForm(initial={
            'delivery_address': f"{request.user.profile.address_1}, {request.user.profile.address_2}, {request.user.profile.city}, {request.user.profile.state}",
        })
    context = {
        'form': form
    }

    return render(request, 'app/fuelform.html', context)


@login_required
def fuel_history(request):
    context = {
        'quotes': FuelQuote.objects.filter(user=request.user),
    }
    return render(request, 'app/FuelQuoteHistory.html', context)


@login_required
@csrf_exempt
@require_POST
def get_price_and_total(request):
    data = json.loads(request.body.decode('utf-8'))
    # print(data)
    location = data.get('delivery_address')
    gallons_requested = float(data.get('gallons_requested'))
    rate = float(data.get('rate'))

    def get_location_factor(location):
        if 'texas' in location.lower():
            location_factor = 0.02

        else:
            location_factor = 0.04
        return location_factor

    def get_rate_history_factor(user):
        if user.fuelquote_set.exists():
            return 0.01
        return 0

    def get_gallons_requested_factor(g):
        if g > 1000:
            return 0.02
        return 0.03

    def get_company_profit_factor():
        return 0.1

    def get_margin(rate):
        margin = rate * (
                    get_location_factor(location) - get_rate_history_factor(request.user) + get_gallons_requested_factor(gallons_requested) + get_company_profit_factor())
        return margin

    def get_suggeted_price_per_gallon(r):
        return r + get_margin(r)

    def get_total(gallons):
        return gallons * get_suggeted_price_per_gallon(rate)

    return JsonResponse(data={
        'suggested_price': round(get_suggeted_price_per_gallon(rate), 4),
        'total': get_total(gallons_requested)
    })