from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from booking.models import *
from django.contrib.admin.views.decorators import staff_member_required
from .forms import FlightForm
# Create your views here.
def admindex(request):
    return render(request,"admindex.html")
def admsignup(request):
    if request.method=='POST':
        uname=request.POST.get('name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1!=pass2:
            messages.warning(request,"Password is Incorrect")
            return redirect('/admsignup')
        try:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"Username is already taken")
                return redirect('/admsignup')
        except:
            pass
        try:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email is already registered")
                return redirect('/admsignup')
        except:
            pass
        user = User.objects.create_user(username=uname, email=email, password=pass1)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        messages.info(request,'User Created Successfully')
        return redirect('/admlogin')
    return render(request, "admsignup.html")

def admlogin(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(request, username=uname, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            if myuser.is_staff:
                return redirect('admindex')
            else:
                return redirect('admlogin')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("admlogin")

    return render(request, "admlogin.html")

@login_required
@staff_member_required
def dashboard(request):
    flights = Flight.objects.all()
    context = {
        'flights': flights,
    }
    return render(request, 'dashboard.html', context)

@login_required
def admlogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('admindex')

@login_required
@staff_member_required
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = FlightForm()
    
    return render(request, 'add_flight.html', {'form': form})

@login_required
@staff_member_required
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id)
    
    if request.method == 'POST':
        flight.delete()
        return redirect('dashboard')
    
    return render(request, 'delete_flight.html', {'flight': flight})

@login_required
@staff_member_required
def admin_search_flights(request):
    if request.method == 'POST':
        flight_number = request.POST.get('flight_number')
        departure_time = request.POST.get('deptime')
        arrival_time = request.POST.get('arrtime')
        flights = Flight.objects.filter(flight_number=flight_number,
                                        depart_time=departure_time,
                                        arrival_time=arrival_time)

        if flights:
            return render(request, 'adminsearch.html', {'flights': flights})
        else:
            return render(request, 'adminsearch.html')

    return render(request, 'adminsearch.html')

