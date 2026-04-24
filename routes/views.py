from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from .models import Station, Route


def index(request):
    """Display all routes with optional search filter"""
    routes = Route.objects.all()
    
    # Search/filter functionality
    origin_filter = request.GET.get('origin')
    destination_filter = request.GET.get('destination')
    
    if origin_filter:
        routes = routes.filter(origin__name__icontains=origin_filter)
    if destination_filter:
        routes = routes.filter(destination__name__icontains=destination_filter)
    
    # Get all unique stations for filter options
    stations = Station.objects.all()
    
    return render(request, 'routes/index.html', {
        'routes': routes,
        'stations': stations,
        'origin_filter': origin_filter,
        'destination_filter': destination_filter
    })


def route(request, route_id):
    """Display route details and passenger list"""
    route = Route.objects.get(id=route_id)
    passengers = route.passengers.all()
    return render(request, 'routes/route.html', {'route': route, 'passengers': passengers})


def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        
        if password != confirmation:
            return render(request, 'routes/register.html', {'message': 'Passwords must match.'})
        
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
        except:
            return render(request, 'routes/register.html', {'message': 'Username already taken.'})
    
    return render(request, 'routes/register.html')


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'routes/login.html', {'message': 'Invalid credentials.'})
    
    return render(request, 'routes/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('index')


@login_required(login_url='login')
@require_http_methods(["POST"])
def book(request, route_id):
    """Book a user on a route"""
    route = Route.objects.get(id=route_id)
    route.passengers.add(request.user)
    return redirect('route', route_id=route_id)


@login_required(login_url='login')
@require_http_methods(["POST"])
def unbook(request, route_id):
    """Remove a user from a route"""
    route = Route.objects.get(id=route_id)
    route.passengers.remove(request.user)
    return redirect('route', route_id=route_id)


@login_required(login_url='login')
def my_routes(request):
    """Display routes booked by the logged-in user"""
    booked_routes = request.user.booked_routes.all()
    return render(request, 'routes/my_routes.html', {'booked_routes': booked_routes})


def station(request, station_id):
    """Display details for a specific station"""
    station = Station.objects.get(id=station_id)
    routes_from = Route.objects.filter(origin=station)
    routes_to = Route.objects.filter(destination=station)
    return render(request, 'routes/station.html', {
        'station': station,
        'routes_from': routes_from,
        'routes_to': routes_to
    })
