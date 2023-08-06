from django.contrib.contenttypes.models import ContentType
from django.forms import (
    CharField, FloatField
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)

from netbox_storage.models import LinuxDevice
from utilities.forms import DynamicModelChoiceField


class LinuxDeviceForm(NetBoxModelForm):
    device = CharField(
        label="Device Name",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )
    type = CharField(
        label="Device Type",
        help_text="The type of the device e.g. Disk, Partition, LVM",
        max_length=255,
    )
    size = FloatField(
        label="Size",
        help_text="The size of the device e.g. 200",
    )
    parent_object = DynamicModelChoiceField(
        queryset=LinuxDevice.objects.all(),
        label="Parent Object",
        help_text="The parent Object of the Device e.g. Drive, LinuxDevice, LV",
    )

    class Meta:
        model = LinuxDevice

        fields = (
            "device",
            "type",
            "size",
        )

    def save(self, *args, **kwargs):
        object_pk = self.cleaned_data['parent_object'].pk

        self.instance.content_type_pk = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
        self.instance.object_id = object_pk

        linux_device = super().save(*args, **kwargs)

        return linux_device


class LinuxDeviceFilterForm(NetBoxModelFilterSetForm):

    model = LinuxDevice

    device = CharField(
        label="Device",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )


class LinuxDeviceImportForm(NetBoxModelImportForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = LinuxDevice

        fields = (
            "device",
            "type",
        )


class LinuxDeviceBulkEditForm(NetBoxModelBulkEditForm):
    model = LinuxDevice

    device = CharField(
        required=False,
        label="Device",
    )
    type = CharField(
        required=False,
        label="Type",
    )

    fieldsets = (
        (
            None,
            ("device", "type"),
        ),
    )
