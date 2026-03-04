from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_room, name='book_room'),
    path('checkout/', views.checkout_room, name='checkout_room'),
    path('available/', views.available_rooms, name='available_rooms'),
    path('waiting_list/', views.view_waiting_list, name='waiting_list'),
    path('history/', views.view_history, name='reservation_history'),
    path('search/', views.search_reservation, name='search_reservation'),
]
