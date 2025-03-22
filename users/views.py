from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import User
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, UserSerializer

class EmployeeListView(ListAPIView):
    queryset = User.objects.filter(is_active=True, is_employee=True)
    serializer_class = UserSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
