from django.urls import path
from . import views

urlpatterns=[
    path('admindex',views.admindex,name='admindex'),
    path('admsignup',views.admsignup,name='admsignup'),
    path('admlogin',views.admlogin,name='admlogin'),
    path('admlogout',views.admlogout,name='admlogout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('admadd',views.add_flight,name='admadd'),
    path('admdelete/<int:flight_id>', views.delete_flight, name='delete_flight'),
    path('admsearch',views.admin_search_flights,name='admsearch'),
]