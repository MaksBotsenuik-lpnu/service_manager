from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Count

from .forms import (
    ClientForm, DeviceForm, ServiceForm, RepairOrderForm, PartForm, ServiceToPartFormSet, RepairOrderServiceFormSet
)
from .models import (
    Client, Device, Service, RepairOrder, Part, ServiceToPart, RepairOrderService
)
from logs.utils import create_log
from logs.models.log import Log


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager


# Client Views
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'service/client_list.html'
    context_object_name = 'clients'
    ordering = ['-created_at']


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'service/client_detail.html'
    success_url = reverse_lazy('service:client-list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'service/client_form.html'
    success_url = reverse_lazy('service:client-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_log(self.request.user, f"Created Client: {self.object}")
        return response


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'service/client_form.html'
    success_url = reverse_lazy('service:client-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_log(self.request.user, f"Updated Client: {self.object}")
        return response


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'service/client_confirm_delete.html'
    success_url = reverse_lazy('service:client-list')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().post(request, *args, **kwargs)
        create_log(request.user, f"Deleted Client: {obj}")
        return response


# Device Views
class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'service/device_list.html'
    context_object_name = 'devices'
    ordering = ['-created_at']


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = 'service/device_detail.html'


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'service/device_form.html'
    success_url = reverse_lazy('service:device-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_log(self.request.user, f"Created Device: {self.object}")
        return response


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'service/device_form.html'
    success_url = reverse_lazy('service:device-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_log(self.request.user, f"Updated Device: {self.object}")
        return response


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    template_name = 'service/device_confirm_delete.html'
    success_url = reverse_lazy('service:device-list')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().post(request, *args, **kwargs)
        create_log(request.user, f"Deleted Device: {obj}")
        return response


# Service Views
class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'service/service_list.html'
    context_object_name = 'services'
    ordering = ['name']


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'service/service_detail.html'


class ServiceCreateView(ManagerRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_form.html'
    success_url = reverse_lazy('service:service-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ServiceToPartFormSet(self.request.POST, prefix='service_parts')
        else:
            context['formset'] = ServiceToPartFormSet(prefix='service_parts')
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ServiceToPartFormSet(self.request.POST, prefix='service_parts')

        if not form.is_valid():
            return self.form_invalid(form, formset)

        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.save()
                
                # Explicitly create ServiceToPart instances
                if formset.is_valid():
                    for part_form in formset:
                        if part_form.cleaned_data and not part_form.cleaned_data.get('DELETE', False):
                            ServiceToPart.objects.create(
                                service=self.object,
                                part=part_form.cleaned_data['part'],
                                part_amount=part_form.cleaned_data['part_amount']
                            )
                create_log(self.request.user, f"Created Service: {self.object}")
                return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class ServiceUpdateView(ManagerRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_form.html'
    success_url = reverse_lazy('service:service-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ServiceToPartFormSet(self.request.POST, instance=self.object, prefix='service_parts')
        else:
            context['formset'] = ServiceToPartFormSet(instance=self.object, prefix='service_parts')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ServiceToPartFormSet(self.request.POST, instance=self.object, prefix='service_parts')

        if not form.is_valid():
            return self.form_invalid(form, formset)

        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.save()
                
                # Remove old ServiceToPart records
                ServiceToPart.objects.filter(service=self.object).delete()
                
                # Explicitly create new ServiceToPart instances
                if formset.is_valid():
                    for part_form in formset:
                        if part_form.cleaned_data and not part_form.cleaned_data.get('DELETE', False):
                            ServiceToPart.objects.create(
                                service=self.object,
                                part=part_form.cleaned_data['part'],
                                part_amount=part_form.cleaned_data['part_amount']
                            )
                create_log(self.request.user, f"Updated Service: {self.object}")
                return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            return self.form_invalid(form, formset)

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class ServiceDeleteView(ManagerRequiredMixin, DeleteView):
    model = Service
    template_name = 'service/service_confirm_delete.html'
    success_url = reverse_lazy('service:service-list')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().post(request, *args, **kwargs)
        create_log(request.user, f"Deleted Service: {obj}")
        return response


# Repair Order Views
class RepairOrderListView(LoginRequiredMixin, ListView):
    model = RepairOrder
    template_name = 'service/repair_order_list.html'
    context_object_name = 'repair_orders'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_manager:
            queryset = queryset.filter(assigned_to=self.request.user)
        return queryset.select_related('device', 'device__client', 'client', 'assigned_to')\
                       .annotate(service_count=Count('order_services'))


class RepairOrderDetailView(LoginRequiredMixin, DetailView):
    model = RepairOrder
    template_name = 'service/repair_order_detail.html'
    context_object_name = 'repair_order'


class RepairOrderCreateView(LoginRequiredMixin, CreateView):
    model = RepairOrder
    form_class = RepairOrderForm
    template_name = 'service/repair_order_form.html'
    success_url = reverse_lazy('service:repair-order-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = RepairOrderServiceFormSet(self.request.POST, prefix='order_services')
        else:
            context['formset'] = RepairOrderServiceFormSet(prefix='order_services')
        return context

    def form_valid(self, form):
        # Set status to pending on create
        form.instance.status = 'pending'
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            # Remove old links just in case (shouldn't be any on create)
            self.object.order_services.all().delete()
            for service_form in formset:
                if service_form.cleaned_data and not service_form.cleaned_data.get('DELETE', False):
                    RepairOrderService.objects.create(
                        repair_order=self.object,
                        service=service_form.cleaned_data['service']
                    )
            # Recalculate final_sum after services are attached
            self.object.final_sum = sum(
                ros.service.price for ros in self.object.order_services.all()
            )
            self.object.save(update_fields=['final_sum'])
            create_log(self.request.user, f"Created RepairOrder: {self.object}")
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class RepairOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = RepairOrder
    form_class = RepairOrderForm
    template_name = 'service/repair_order_form.html'
    success_url = reverse_lazy('service:repair-order-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = RepairOrderServiceFormSet(self.request.POST, instance=self.object, prefix='order_services')
        else:
            context['formset'] = RepairOrderServiceFormSet(instance=self.object, prefix='order_services')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object:
            form.fields['device'].queryset = Device.objects.filter(client=self.object.client)
        return form

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            response = super().form_valid(form)
            # Remove old links
            self.object.order_services.all().delete()
            for service_form in formset:
                if service_form.cleaned_data and not service_form.cleaned_data.get('DELETE', False):
                    RepairOrderService.objects.create(
                        repair_order=self.object,
                        service=service_form.cleaned_data['service']
                    )
            # Recalculate final_sum after services are attached
            self.object.final_sum = sum(
                ros.service.price for ros in self.object.order_services.all()
            )
            self.object.save(update_fields=['final_sum'])
            create_log(self.request.user, f"Updated RepairOrder: {self.object}")
            return response
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class RepairOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = RepairOrder
    template_name = 'service/repair_order_confirm_delete.html'
    success_url = reverse_lazy('service:repair-order-list')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().post(request, *args, **kwargs)
        create_log(request.user, f"Deleted RepairOrder: {obj}")
        return response


# Part Views
class PartListView(LoginRequiredMixin, ListView):
    model = Part
    template_name = 'service/part_list.html'
    context_object_name = 'parts'
    ordering = ['part_type', 'brand', 'name']


class PartDetailView(LoginRequiredMixin, DetailView):
    model = Part
    template_name = 'service/part_detail.html'


class PartCreateView(LoginRequiredMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'service/part_form.html'
    success_url = reverse_lazy('service:part-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_log(self.request.user, f"Created Part: {self.object}")
        return response


class PartUpdateView(LoginRequiredMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'service/part_form.html'
    success_url = reverse_lazy('service:part-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_log(self.request.user, f"Updated Part: {self.object}")
        return response


class PartDeleteView(LoginRequiredMixin, DeleteView):
    model = Part
    template_name = 'service/part_confirm_delete.html'
    success_url = reverse_lazy('service:part-list')

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        response = super().post(request, *args, **kwargs)
        create_log(request.user, f"Deleted Part: {obj}")
        return response


@csrf_exempt
@require_GET
def get_client_devices(request, client_id):
    """Get devices for a specific client."""
    try:
        devices = Device.objects.filter(client_id=client_id).values('id', 'brand', 'model')
        return JsonResponse(list(devices), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
