import django_tables2 as tables

from netbox.tables import (
    NetBoxTable,
    ToggleColumn,
)
from netbox_storage.models import MountedVolume


class MountedVolumeTable(NetBoxTable):

    pk = ToggleColumn()
    fs_type = tables.Column(
        linkify=True,
        verbose_name="Filesystem"
    )
    mount_point = tables.Column(
        linkify=True,
        verbose_name="Mount point"
    )

    class Meta(NetBoxTable.Meta):
        model = MountedVolume
        fields = (
            "pk",
            "mount_point",
            "fs_type",
            "options",
            "description",
        )
        default_columns = (
            "mount_point",
            "fs_type",
            "options",
            "description",
        )
