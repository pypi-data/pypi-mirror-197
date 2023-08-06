from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import LogicalVolume


class LogicalVolumeTable(NetBoxTable):
    """Table for displaying LogicalVolume objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = LogicalVolume
        fields = (
            "pk",
            "vg",
            "lv_name",
            "size",
            "device",
            "description",
        )
        default_columns = (
            "vg",
            "lv_name",
            "size",
            "device",
            "description",
        )
