from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Machine, Maintenance, Complaint, VehicleModel, EngineModel, 
    TransmissionModel, DriveAxleModel, SteeringAxleModel, 
    MaintenanceType, FailureNode, RecoveryMethod, ServiceCompany,
    MaintenanceOrganization
)
from .serializers import MachineSerializer, MaintenanceSerializer, ComplaintSerializer

class MainPageView(ListView):
    model = Machine
    template_name = 'silant/main.html'
    context_object_name = 'machines'

    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            vin_query = self.request.GET.get('vin')
            if vin_query:
                return Machine.objects.filter(vin__iexact=vin_query)
            return Machine.objects.none()
            
        if user.is_staff or user.is_superuser:
            qs = Machine.objects.all().order_by('-shipping_date')
        elif hasattr(user, 'service_profile'):
            qs = Machine.objects.filter(service_company=user.service_profile).order_by('-shipping_date')
        else:
            qs = Machine.objects.filter(client=user).order_by('-shipping_date')

        v_model = self.request.GET.get('v_model')
        e_model = self.request.GET.get('e_model')
        transmission_model = self.request.GET.get('transmission_model')
        steering_axle_model = self.request.GET.get('steering_axle_model')
        drive_axle_model = self.request.GET.get('drive_axle_model')

        if v_model: qs = qs.filter(vehicle_model_id=v_model)
        if e_model: qs = qs.filter(engine_model_id=e_model)
        if transmission_model: qs = qs.filter(transmission_model_id=transmission_model)
        if steering_axle_model: qs = qs.filter(steering_axle_model_id=steering_axle_model)
        if drive_axle_model: qs = qs.filter(drive_axle_model_id=drive_axle_model)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        vin_query = self.request.GET.get('vin', '')
        context['vin_query'] = vin_query
        
        if vin_query and not self.get_queryset().exists():
            context['search_failed'] = True
        else:
            context['search_failed'] = False
        
        context['v_models'] = VehicleModel.objects.all()
        context['e_models'] = EngineModel.objects.all()
        context['transmission_models'] = TransmissionModel.objects.all()
        context['steering_axle_models'] = SteeringAxleModel.objects.all()
        context['drive_axle_models'] = DriveAxleModel.objects.all()
        context['companies'] = ServiceCompany.objects.all()
        context['mt_types'] = MaintenanceType.objects.all()
        context['mt_orgs'] = MaintenanceOrganization.objects.all()
        context['f_nodes'] = FailureNode.objects.all()
        context['r_methods'] = RecoveryMethod.objects.all()

        context['selected_v_model'] = self.request.GET.get('v_model', '')
        context['selected_e_model'] = self.request.GET.get('e_model', '')
        context['selected_transmission_model'] = self.request.GET.get('transmission_model', '')
        context['selected_steering_axle_model'] = self.request.GET.get('steering_axle_model', '')
        context['selected_drive_axle_model'] = self.request.GET.get('drive_axle_model', '')
        context['selected_company'] = self.request.GET.get('company', '')
        context['selected_mt_type'] = self.request.GET.get('mt_type', '')
        context['selected_mt_org'] = self.request.GET.get('mt_org', '')
        context['selected_f_node'] = self.request.GET.get('f_node', '')
        context['selected_r_method'] = self.request.GET.get('r_method', '')

        if user.is_authenticated:
            if user.is_staff or user.is_superuser:
                maintenances = Maintenance.objects.all().select_related('machine', 'maintenance_type', 'service_company')
            elif hasattr(user, 'service_profile'):
                maintenances = Maintenance.objects.filter(service_company=user.service_profile).select_related('machine', 'maintenance_type', 'service_company')
            else:
                maintenances = Maintenance.objects.filter(machine__client=user).select_related('machine', 'maintenance_type', 'service_company')

            if user.is_staff or user.is_superuser:
                complaints = Complaint.objects.all().select_related('machine', 'failure_node', 'recovery_method', 'service_company')
            elif hasattr(user, 'service_profile'):
                complaints = Complaint.objects.filter(service_company=user.service_profile).select_related('machine', 'failure_node', 'recovery_method', 'service_company')
            else:
                complaints = Complaint.objects.filter(machine__client=user).select_related('machine', 'failure_node', 'recovery_method', 'service_company')

            mt_type = self.request.GET.get('mt_type')
            vin_num = self.request.GET.get('vin_num')
            company = self.request.GET.get('company')
            
            if mt_type: maintenances = maintenances.filter(maintenance_type_id=mt_type)
            if vin_num: maintenances = maintenances.filter(machine__vin__iexact=vin_num)
            if company: maintenances = maintenances.filter(service_company_id=company)

            f_node = self.request.GET.get('f_node')
            r_method = self.request.GET.get('r_method')
            comp_company = self.request.GET.get('comp_company')
            
            if f_node: complaints = complaints.filter(failure_node_id=f_node)
            if r_method: complaints = complaints.filter(recovery_method_id=r_method)
            if comp_company: complaints = complaints.filter(service_company_id=comp_company)

            context['maintenances'] = list(maintenances.order_by('-maintenance_date'))
            context['complaints'] = list(complaints.order_by('-failure_date'))
                
        return context

class MachineDetailView(LoginRequiredMixin, DetailView):
    model = Machine
    template_name = 'silant/machine_detail.html'
    context_object_name = 'machine'

class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = Maintenance
    template_name = 'silant/maintenance_detail.html'
    context_object_name = 'mt'

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = 'silant/complaint_detail.html'
    context_object_name = 'cp'

class MachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Machine.objects.all()
        if hasattr(user, 'service_profile'):
            return Machine.objects.filter(service_company=user.service_profile)
        return Machine.objects.filter(client=user)

class MaintenanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Maintenance.objects.all()
        if hasattr(user, 'service_profile'):
            return Maintenance.objects.filter(service_company=user.service_profile)
        return Maintenance.objects.filter(machine__client=user)

class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Complaint.objects.all()
        if hasattr(user, 'service_profile'):
            return Complaint.objects.filter(service_company=user.service_profile)
        return Complaint.objects.filter(machine__client=user)




