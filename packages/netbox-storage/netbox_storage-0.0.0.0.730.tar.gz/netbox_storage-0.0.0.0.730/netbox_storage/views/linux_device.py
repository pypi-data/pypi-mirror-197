from netbox.views import generic

from netbox_storage.filters import LinuxDeviceFilter
from netbox_storage.forms import (
    LinuxDeviceImportForm,
    LinuxDeviceFilterForm,
    LinuxDeviceForm,
    LinuxDeviceBulkEditForm
)

from netbox_storage.models import LinuxDevice
from netbox_storage.tables import LinuxDeviceTable


class LinuxDeviceListView(generic.ObjectListView):
    queryset = LinuxDevice.objects.all()
    filterset = LinuxDeviceFilter
    filterset_form = LinuxDeviceFilterForm
    table = LinuxDeviceTable


class LinuxDeviceView(generic.ObjectView):
    queryset = LinuxDevice.objects.all()


class LinuxDeviceEditView(generic.ObjectEditView):

    queryset = LinuxDevice.objects.all()
    form = LinuxDeviceForm
    default_return_url = "plugins:netbox_storage:linuxdevice_list"


class LinuxDeviceDeleteView(generic.ObjectDeleteView):
    queryset = LinuxDevice.objects.all()
    default_return_url = "plugins:netbox_storage:linuxdevice_list"


class LinuxDeviceBulkImportView(generic.BulkImportView):
    queryset = LinuxDevice.objects.all()
    model_form = LinuxDeviceImportForm
    table = LinuxDeviceTable
    default_return_url = "plugins:netbox_storage:linuxdevice_list"


class LinuxDeviceBulkEditView(generic.BulkEditView):
    queryset = LinuxDevice.objects.all()
    filterset = LinuxDeviceFilter
    table = LinuxDeviceTable
    form = LinuxDeviceBulkEditForm


class LinuxDeviceBulkDeleteView(generic.BulkDeleteView):
    queryset = LinuxDevice.objects.all()
    table = LinuxDeviceTable
