from django.contrib import admin
from .models import (
    VehicleModel, EngineModel, TransmissionModel, DriveAxleModel, 
    SteeringAxleModel, MaintenanceType, FailureNode, RecoveryMethod, 
    MaintenanceOrganization, ServiceCompany, Machine, Maintenance, Complaint
)

@admin.register(VehicleModel, EngineModel, TransmissionModel, DriveAxleModel, 
                SteeringAxleModel, MaintenanceType, FailureNode, RecoveryMethod,
                MaintenanceOrganization)
class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('directory_name', 'name', 'description')
    list_filter = ('directory_name',)
    search_fields = ('name', 'directory_name')

@admin.register(ServiceCompany)
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'description')
    search_fields = ('name',)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('vin', 'vehicle_model', 'shipping_date', 'client', 'service_company')
    list_filter = ('vehicle_model', 'engine_model', 'service_company')
    search_fields = ('vin', 'consignee')
    fieldsets = (
        ('Общая информация (доступна анонимам)', {
            'fields': ('vin', 'vehicle_model', 'engine_model', 'engine_num', 
                       'transmission_model', 'transmission_num', 'drive_axle_model', 
                       'drive_axle_num', 'steering_axle_model', 'steering_axle_num')
        }),
        ('Конфиденциальные данные', {
            'fields': ('delivery_contract', 'shipping_date', 'consignee', 
                       'delivery_address', 'equipment', 'client', 'service_company')
        }),
    )

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'maintenance_org', 'service_company')
    list_filter = ('maintenance_type', 'service_company', 'maintenance_date', 'maintenance_org')
    search_fields = ('machine__vin', 'order_number')
    readonly_fields = ('service_company',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_date', 'failure_node', 'recovery_method', 'parts_used', 'downtime', 'service_company')
    list_filter = ('failure_node', 'recovery_method', 'failure_date', 'service_company')
    search_fields = ('machine__vin', 'failure_description')
    readonly_fields = ('downtime', 'service_company')


