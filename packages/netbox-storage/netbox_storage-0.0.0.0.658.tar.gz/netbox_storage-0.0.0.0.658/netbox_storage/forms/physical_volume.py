from django.core.validators import MinValueValidator
from django.forms import (
    CharField,
    FloatField,
)
from django.urls import reverse_lazy

from netbox.forms import (
    NetBoxModelBulkEditForm,
    NetBoxModelFilterSetForm,
    NetBoxModelImportForm,
    NetBoxModelForm,
)
from utilities.forms import (
    DynamicModelChoiceField, APISelect,
)

from netbox_storage.models import Drive, PhysicalVolume


class PhysicalVolumeForm(NetBoxModelForm):
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            "description",
        )


class PhysicalVolumeFilterForm(NetBoxModelFilterSetForm):

    model = PhysicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )


class PhysicalVolumeImportForm(NetBoxModelImportForm):

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = PhysicalVolume

        fields = (
            "description",
        )


class PhysicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = PhysicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. PhysicalVolume 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ["description"]
        ),
    )
    nullable_fields = ["description"]
