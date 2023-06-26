from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):
    flight_id = models.IntegerField(primary_key=True, editable=False)
    flight_number = models.CharField(max_length=10, unique=True, default=None)
    flight_name = models.CharField(max_length=100, default=None)
    depart_date = models.DateField(default=None)
    depart_time = models.TimeField(default=None)
    depart_loc = models.CharField(max_length=100, default=None)
    total_seats = models.IntegerField(default=60)
    duration = models.CharField(max_length=50, default=None)
    arrival_date = models.DateField(default=None)
    arrival_time = models.TimeField(default=None)
    arrival_loc = models.CharField(max_length=100, default=None)
    price = models.IntegerField(default=None)
    logo = models.ImageField(upload_to="files/thumbnail", default=None)

    def __str__(self):
        return self.flight_number
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='bookings')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.booked_flight.flight_number}'
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name