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

from netbox_storage.models import Drive, LogicalVolume


class LogicalVolumeForm(NetBoxModelForm):
    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = LogicalVolume

        fields = (
            "description",
        )


class LogicalVolumeFilterForm(NetBoxModelFilterSetForm):

    model = LogicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )


class LogicalVolumeImportForm(NetBoxModelImportForm):

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )

    class Meta:
        model = LogicalVolume

        fields = (
            "description",
        )


class LogicalVolumeBulkEditForm(NetBoxModelBulkEditForm):
    model = LogicalVolume

    description = CharField(
        required=False,
        label="Description",
        help_text="Short Description e.g. LogicalVolume 1 on SSD Cluster",
    )

    fieldsets = (
        (
            None,
            ["description"]
        ),
    )
    nullable_fields = ["description"]
