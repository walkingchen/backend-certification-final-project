# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookingForm, UserRegistrationForm
from .models import Menu, Booking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime



# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@csrf_exempt
def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Check for duplicate booking
            reservation_date = form.cleaned_data['reservation_date']
            reservation_slot = form.cleaned_data['reservation_slot']
            
            # Check if the same date and time slot already has a booking
            existing_booking = Booking.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=reservation_slot
            ).first()
            
            if existing_booking:
                # Return error message
                return JsonResponse({
                    'success': False,
                    'message': f'The date {reservation_date} and time slot {reservation_slot} is already booked'
                })
            
            form.save()
            return JsonResponse({'success': True, 'message': 'Booking successful!'})
        else:
            # Form validation failed, return error message
            errors = []
            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(f"{field}: {error}")
            return JsonResponse({
                'success': False,
                'message': 'Form validation failed: ' + '; '.join(errors)
            })
    context = {'form':form}
    return render(request, 'book.html', context)

@csrf_exempt
def reservations_api(request):
    """API endpoint: Returns booking data for a specific date"""
    if request.method == 'GET':
        date_str = request.GET.get('date')
        if date_str:
            try:
                # Parse date
                reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                # Get all bookings for this date
                bookings = Booking.objects.filter(reservation_date=reservation_date)
                
                if bookings.exists():
                    booking_data = []
                    for booking in bookings:
                        booking_data.append({
                            'id': booking.id,
                            'first_name': booking.first_name,
                            'reservation_slot': booking.reservation_slot,
                            'created_at': booking.id  # Use id as creation time identifier
                        })
                    return JsonResponse({
                        'success': True,
                        'date': date_str,
                        'bookings': booking_data
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'date': date_str,
                        'bookings': [],
                        'message': 'No Booking'
                    })
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid date format'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please provide a date parameter'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Only GET requests are supported'
    })

# Add your code here to create new views
# New: menu view function
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {
        "menu": menu_data
    }
    return render(request, 'menu.html', main_data)

# New: display_menu_item view function
def display_menu_item(request, pk=None):
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    else:
        menu_item = ''
    return render(request, 'menu_item.html', {"menu_item": menu_item})


# User authentication views
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Little Lemon.')
            return redirect('home')
        else:
            messages.error(request, 'Registration failed, please check your information.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password.')
    
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')


@login_required
def profile(request):
    user_bookings = Booking.objects.filter(
        first_name=request.user.first_name or request.user.username,
        last_name=request.user.last_name or ''
    )
    return render(request, 'profile.html', {'bookings': user_bookings})