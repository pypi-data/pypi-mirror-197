from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import VolumeGroup


class VolumeGroupTable(NetBoxTable):
    """Table for displaying VolumeGroup objects."""

    pk = ToggleColumn()

    class Meta(NetBoxTable.Meta):
        model = VolumeGroup
        fields = (
            "pk",
            "vg_name",
            "description",
        )
        default_columns = (
            "vg_name",
            "description",
        )
