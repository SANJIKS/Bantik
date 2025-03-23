from datetime import datetime, timedelta
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import make_aware
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, UserSerializer
from services.models import Service, Appointment

class EmployeeListView(ListAPIView):
    queryset = User.objects.filter(is_active=True, is_employee=True)
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['services']

    def get_queryset(self):
        queryset = super().get_queryset()
        service_id = self.request.query_params.get('service')
        date_str = self.request.query_params.get('date')
        time_str = self.request.query_params.get('time')

        if service_id:
            queryset = queryset.filter(services__id=service_id)

        if date_str and time_str:
            try:
                date_time = make_aware(datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M"))
                service = Service.objects.filter(id=service_id).first()

                if service:
                    service_duration = timedelta(minutes=service.duration)

                    busy_masters = Appointment.objects.filter(
                        Q(date_time__lt=date_time + service_duration, date_time__gte=date_time)
                    ).values_list('master_id', flat=True)

                    queryset = queryset.exclude(id__in=busy_masters)

            except ValueError:
                pass

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'service',
                openapi.IN_QUERY,
                description="Фильтрация по ID услуги",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Дата в формате ДД-ММ-ГГГГ",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'time',
                openapi.IN_QUERY,
                description="Время в формате ЧЧ:ММ",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class EmployeeRetrieveView(RetrieveAPIView):
    queryset = User.objects.filter(is_active=True, is_employee=True)
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
