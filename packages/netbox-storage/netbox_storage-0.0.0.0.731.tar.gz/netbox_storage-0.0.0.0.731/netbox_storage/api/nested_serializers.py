from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from netbox_storage.models import Filesystem, Drive, Partition, MountedVolume, LinuxDevice


#
# Device
#
class NestedDeviceSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:linuxdevice-detail"
    )

    class Meta:
        model = LinuxDevice
        fields = ["id", "url", "display", "device", "type"]


#
# Filesystem
#

class NestedFilesystemSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:filesystem-detail"
    )

    class Meta:
        model = Filesystem
        fields = ["id", "url", "display", "filesystem"]


#
# Drive
#
class NestedDriveSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:drive-detail"
    )

    class Meta:
        model = Drive
        fields = ["id", "url", "display", "size", "identifier"]


#
# Partition
#
class NestedPartitionSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:partition-detail"
    )

    class Meta:
        model = Partition
        fields = ["id", "url", "display", "size", "device", "type"]


#
# Linux Volume
#
class NestedMountedVolumeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:mountedvolume-detail"
    )

    class Meta:
        model = MountedVolume
        fields = ["id", "url", "display", "mount_point"]


class NestedVolumeGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_storage-api:volumegroup-detail"
    )

    class Meta:
        model = MountedVolume
        fields = ["id", "url", "display"]
