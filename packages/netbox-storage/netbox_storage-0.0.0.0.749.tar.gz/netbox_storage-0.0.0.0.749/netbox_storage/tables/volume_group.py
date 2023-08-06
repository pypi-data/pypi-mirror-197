from django_tables2 import tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)

from netbox_storage.models import VolumeGroup


class VolumeGroupTable(NetBoxTable):
    """Table for displaying VolumeGroup objects."""

    pk = ToggleColumn()
    vg_name = tables.Column(
        linkify=True
    )

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
