from django.contrib.contenttypes.models import ContentType

from extras.plugins import PluginTemplateExtension
from netbox_storage.models import LogicalVolume, StorageConfigurationDrive, \
    TemplateConfigurationDrive, Drive, Partition, LinuxDevice, MountedVolume


class RelatedDrives(PluginTemplateExtension):
    model = "virtualization.virtualmachine"

    def left_page(self):
        obj = self.context.get("object")

        lv = LogicalVolume.objects.all()

        storage_configuration = StorageConfigurationDrive.objects.filter(virtual_machine=obj)

        platform = obj.platform
        if platform is not None:
            if platform.name.lower().__contains__('windows'):
                return self.render(
                    "netbox_storage/inc/windowsvolume_box.html",
                    extra_context={
                        # "volumes": volumes,
                        # "unmapped_drives": unmapped_drives,
                        "type": type(obj.platform),
                    },
                )
            elif platform.name.lower().__contains__('linux'):
                return self.render(
                    "netbox_storage/inc/linuxvolume_box.html"
                )
        else:
            return self.render(
                "netbox_storage/inc/unknown_os_box.html",
                extra_context={
                    "lv": lv,
                    "storage_configuration": storage_configuration
                }
            )


class TemplateVolumeConfig(PluginTemplateExtension):
    model = "dcim.platform"

    def right_page(self):
        obj = self.context.get("object")

        drives_id = TemplateConfigurationDrive.objects.values('drive').filter(platform=obj)
        partition_dict = {
        }
        for drive_id in drives_id:
            print(f"Drive ID: {drive_id['drive']}")
            drive = Drive.objects.get(pk=drive_id['drive'])

            drive_type_id = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
            linux_device_type_id = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
            # Get Linux Device of Drive e.g. /dev/sda
            linux_device_drive = LinuxDevice.objects.get(content_type_id=drive_type_id,
                                                         object_id=drive_id['drive'],
                                                         type='Disk')

            if LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                          object_id=linux_device_drive.pk,
                                          type='Partition').count() == 0:
                partition_dict[drive] = None
            else:
                partition_dict[drive] = list(LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                                                        object_id=linux_device_drive.pk,
                                                                        type='Partition'))

        return self.render(
            "netbox_storage/inc/template_drive_box.html",
            extra_context={
                "partition_dict": partition_dict
            }
        )

    def left_page(self):
        mounted_volumes = MountedVolume.objects.all()
        return self.render(
            "netbox_storage/inc/template_volume_box.html",
            extra_context={
                "mounted_volumes": mounted_volumes
            }
        )

    def full_width_page(self):
        obj = self.context.get("object")

        drives = TemplateConfigurationDrive.objects.values('drive').filter(platform=obj)
        drives_id = []
        lonely_drive = []
        linux_devices = []
        for drive_id in drives:
            drives_id.append(drive_id['drive'])
            # if LinuxDevice.objects.filter(linux_device_drives=drive_id['drive']).count() == 0:
            drive = Drive.objects.get(pk=drive_id['drive'])
            lonely_drive.append(drive)
#                print(LinuxDevice.objects.filter(linux_device_drives=drive_id['drive']))

        partitions = Partition.objects.filter(drive_id__in=drives_id)

        return self.render(
            "netbox_storage/inc/template_volume_box.html",
            extra_context={
                "lonely_drives": lonely_drive,
                "partitions": partitions,
                "linux_devices": linux_devices
            }
        )


template_extensions = [RelatedDrives, TemplateVolumeConfig]
