from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, Service
from users.serializers import UserSerializer

User = get_user_model()

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "duration", "price"]

class CreateAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        master = data["master"]
        service = data["service"]

        if service not in master.services.all():
            raise serializers.ValidationError(f"Мастер {master} не предоставляет услугу '{service}'.")

        if Appointment.objects.filter(master=master, date_time=data["date_time"]).exists():
            raise serializers.ValidationError("Этот мастер уже занят на выбранное время.")
        
        return data

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["master", "date_time"]


class AppointmentDetailSerializer(serializers.ModelSerializer):
    master = UserSerializer()
    service = ServiceSerializer()
    
    class Meta:
        model = Appointment
        fields = '__all__'
