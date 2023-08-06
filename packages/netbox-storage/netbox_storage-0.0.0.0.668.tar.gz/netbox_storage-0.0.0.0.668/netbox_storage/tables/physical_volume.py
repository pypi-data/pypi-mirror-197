from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import PhysicalVolume


class PhysicalVolumeTable(NetBoxTable):
    """Table for displaying VolumeGroup objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = PhysicalVolume
        fields = (
            "pk",
            "device",
            "vg",
            "description",
        )
        default_columns = (
            "device",
            "vg",
            "description",
        )
