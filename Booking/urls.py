from django.urls import path
from .views import RegisterTimeSlot, GetAvailableSlots, UserListView

urlpatterns = [
    path('register-timeslot/', RegisterTimeSlot.as_view(), name='register-timeslot'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('get-available-slots/', GetAvailableSlots.as_view(), name='get-available-slots'),
]
