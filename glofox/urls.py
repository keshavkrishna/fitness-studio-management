# urls.py

from django.urls import path
from . import views

urlpatterns = [
    # User Management
    path('users/', views.UserView.as_view(), name='user-list-create'),
    path('users/<int:user_id>/', views.UserView.as_view(), name='user-detail'),
    path('users/<int:user_id>/dashboard/', views.MemberDashboardView.as_view(), name='member-dashboard'),

    # Studio Management
    path('studios/', views.StudioView.as_view(), name='studio-list-create'),
    path('studios/<int:studio_id>/', views.StudioView.as_view(), name='studio-detail'),

    # Class Management
    path('classes/', views.ClassView.as_view(), name='class-list-create'),
    path('classes/<int:class_id>/', views.ClassView.as_view(), name='class-detail'),
    path('classes/<int:class_id>/availability/', views.ClassAvailabilityView.as_view(), name='class-availability'),

    # Booking Management
    path('bookings/', views.BookingView.as_view(), name='booking-list-create'),
    path('bookings/<int:booking_id>/', views.BookingView.as_view(), name='booking-detail'),
       
]