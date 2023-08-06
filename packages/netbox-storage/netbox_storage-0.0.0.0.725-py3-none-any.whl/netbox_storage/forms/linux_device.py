from django.forms import (
    CharField
)

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)

from netbox_storage.models import LinuxDevice


class LinuxDeviceForm(NetBoxModelForm):
    device = CharField(
        label="Device Name",
        help_text="The mounted path of the volume e.g. /var/lib/docker",
    )

    class Meta:
        model = LinuxDevice

        fields = (
            "device",
            "type",
        )

    #def save(self, *args, **kwargs):
    #    new_partition_count = Partition.objects.filter(drive_id=self.cleaned_data['drive'].id).count() + 1
    #    device_name_prefix = Drive.objects.get(pk=self.cleaned_data['drive'].id).device_name()
    #    device_name = device_name_prefix + str(new_partition_count)


     #   return linux_device
        """
        project_owner_pk = ContactRole.objects.get(name='Project Owner').pk
        ocp_project_type_pk = ContentType.objects.get(app_label='ocp_project_plugin', model='ocpproject').pk

        count_assignment = ContactAssignment.objects.filter(object_id=self.pk).count()
        if count_assignment == 0:
            ContactAssignment.objects.create(object_id=self.pk,
                                             contact_id=self.project_owner.pk,
                                             content_type_id=ocp_project_type_pk,
                                             role_id=project_owner_pk)

        """


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
