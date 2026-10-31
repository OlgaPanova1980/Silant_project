from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MainPageView, 
    MachineDetailView, 
    MaintenanceDetailView, 
    ComplaintDetailView,
    MachineViewSet,
    MaintenanceViewSet,
    ComplaintViewSet
)

router = DefaultRouter()
router.register(r'machines', MachineViewSet, basename='api_machine')
router.register(r'maintenance', MaintenanceViewSet, basename='api_maintenance')
router.register(r'complaints', ComplaintViewSet, basename='api_complaint')

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('machine/<int:pk>/', MachineDetailView.as_view(), name='machine_detail'),
    path('maintenance/<int:pk>/', MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('complaint/<int:pk>/', ComplaintDetailView.as_view(), name='complaint_detail'),
    path('api/', include(router.urls)),
]

