from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ContactForm

# Create your views here.
def home(request):
    return render(request,'home.html')
def index(request):
    return render(request,'index.html')

def auth_signup(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.warning(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=uname).exists():
            messages.info(request, "Username is already taken")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.info(request, "Email is already registered")
            return redirect('signup')

        user = User.objects.create_user(username=uname, email=email, password=pass1)
        user.save()
        messages.info(request, 'User created successfully')
        return redirect('login')

    return render(request, 'signup.html')

def auth_login(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(request, username=uname, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/index')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("/login")

    return render(request, "login.html")


@login_required
def auth_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/')

@login_required
def search_flights(request):
    if request.method == 'POST':
        dep_date = request.POST.get('depdate')
        dep_time = request.POST.get('deptime')
        arr_date = request.POST.get('arrdate')
        arr_time = request.POST.get('arrtime')
        flights = Flight.objects.filter(depart_date=dep_date, depart_time=dep_time, arrival_date=arr_date, arrival_time=arr_time)
        return render(request, 'bookings.html', {'flights': flights})
    
    return render(request, 'bookings.html')

@login_required
def book_flight(request, flight_id):
    flight = Flight.objects.get(flight_id=flight_id)
    if flight.total_seats > 0:  # Check if there are available seats on the flight
        if request.method == 'POST':
            booking = Booking(user=request.user, booked_flight=flight)
            booking.save()
            flight.total_seats -= 1  # Reduce the available seat count by 1
            flight.save()
            messages.success(request, "Ticket Booked Successfully")
            return redirect('my_tickets')
    else:
        messages.warning(request, "No available seats for this flight.")
    return redirect('booking')
@login_required
def my_tickets(request):
    bookings=Booking.objects.filter(user=request.user)
    return render(request, 'mytickets.html',{'bookings':bookings})
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for contacting us!. Your message has been successfully submitted")
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
