from django.urls import path
from .views import BusyAppointmentsView, ServiceListView, CreateAppointmentView, AppointmentListView

urlpatterns = [
    path("create-appointment/", CreateAppointmentView.as_view(), name="create-appointment"),
    path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
    path("busy-appointments/", BusyAppointmentsView.as_view(), name="busy-appointments"),
    path("services/", ServiceListView.as_view(), name="service-list"),
]