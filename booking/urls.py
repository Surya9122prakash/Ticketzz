from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('index',views.index,name='index'),
    path('login',views.auth_login,name='login'),
    path('signup',views.auth_signup,name='signup'),
    path('logout',views.auth_logout, name = 'logout'),
    path('booking',views.search_flights,name='booking'),
    path('book_flight/<int:flight_id>', views.book_flight, name='book_flight'),
    path('mytickets/', views.my_tickets, name='mytickets'),
    path('contact/', views.contact, name='contact'),
    path('',include('adminuser.urls')),
]