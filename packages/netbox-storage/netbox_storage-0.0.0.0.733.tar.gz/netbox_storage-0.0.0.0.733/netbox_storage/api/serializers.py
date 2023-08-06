from rest_framework import serializers

from dcim.api.nested_serializers import NestedPlatformSerializer
from netbox.api.serializers import NetBoxModelSerializer
from netbox_storage.api.nested_serializers import NestedFilesystemSerializer, NestedDriveSerializer, \
    NestedMountedVolumeSerializer, NestedDeviceSerializer, NestedVolumeGroupSerializer
from netbox_storage.models import Drive, Filesystem, Partition, MountedVolume, StorageConfigurationDrive, \
    LinuxDevice, TemplateConfigurationDrive, PhysicalVolume, VolumeGroup, LogicalVolume
from virtualization.api.nested_serializers import NestedClusterSerializer, NestedVirtualMachineSerializer


class FilesystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filesystem
        fields = (
            "id",
            "filesystem",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class DriveSerializer(NetBoxModelSerializer):
    cluster = NestedClusterSerializer(required=False, allow_null=True)
    url = serializers.HyperlinkedIdentityField(view_name="plugins-api:netbox_storage-api:drive-detail")

    class Meta:
        model = Drive
        fields = (
            "id",
            "url",
            "display",
            "size",
            "cluster",
            "identifier",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class PartitionSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_storage-api:partition-detail')
    drive = NestedDriveSerializer(required=False, allow_null=True)
    device = NestedDeviceSerializer(required=False, allow_null=True)

    class Meta:
        model = Partition
        fields = (
            "id",
            "url",
            "drive",
            "device",
            "size",
            "type",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class MountedVolumeSerializer(serializers.ModelSerializer):
    fs_type = NestedFilesystemSerializer(required=False, allow_null=True)

    class Meta:
        model = MountedVolume
        fields = (
            "id",
            "mount_point",
            "fs_type",
            "options",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class LinuxDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinuxDevice
        fields = (
            "id",
            "device",
            "type",
            "size",
            "created",
            "last_updated",
            "custom_fields",
        )


class PhysicalVolumeSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer(required=False, allow_null=True)
    vg = NestedVolumeGroupSerializer(required=False, allow_null=True)

    class Meta:
        model = PhysicalVolume
        fields = (
            "id",
            "device",
            "vg",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class VolumeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = VolumeGroup
        fields = (
            "id",
            "vg_name",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class LogicalVolumeSerializer(serializers.ModelSerializer):
    device = NestedDeviceSerializer(required=False, allow_null=True)
    vg = NestedVolumeGroupSerializer(required=False, allow_null=True)

    class Meta:
        model = LogicalVolume
        fields = (
            "id",
            "vg",
            "lv_name",
            "size",
            "device",
            "description",
            "created",
            "last_updated",
            "custom_fields",
        )


class StorageConfigurationDriveSerializer(serializers.ModelSerializer):
    linux_volume = NestedMountedVolumeSerializer(required=False, allow_null=True)
    virtual_machine = NestedVirtualMachineSerializer(required=False, allow_null=True)

    class Meta:
        model = StorageConfigurationDrive
        fields = (
            "id",
            "device",
            "linux_volume",
            "created",
            "last_updated",
            "custom_fields",
        )


class TemplateConfigurationDriveSerializer(serializers.ModelSerializer):
    drive = NestedDriveSerializer(required=False, allow_null=True)
    platform = NestedPlatformSerializer(required=False, allow_null=True)

    class Meta:
        model = TemplateConfigurationDrive
        fields = (
            "id",
            "platform",
            "drive",
            "created",
            "last_updated",
            "custom_fields",
        )
