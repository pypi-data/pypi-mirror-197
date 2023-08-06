import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)
from netbox_storage.models import LinuxDevice


class LinuxDeviceTable(NetBoxTable):

    pk = ToggleColumn()
    device = tables.Column(
        linkify=True,
        verbose_name="Device"
    )
    type = tables.Column(
        linkify=True,
        verbose_name="Type"
    )

    class Meta(NetBoxTable.Meta):
        model = LinuxDevice
        fields = (
            "pk",
            "device",
            "type",
            "mounted_volume",
            "description",
        )
        default_columns = (
            "pk",
            "device",
            "type",
            "mounted_volume",
            "description",
        )
