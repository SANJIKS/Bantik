from django.urls import path, include
from .views import EmployeeListView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('employees/', EmployeeListView.as_view(), name='employees-list')
]
