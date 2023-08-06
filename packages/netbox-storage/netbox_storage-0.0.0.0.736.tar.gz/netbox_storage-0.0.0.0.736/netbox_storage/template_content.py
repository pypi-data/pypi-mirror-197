from django.contrib.contenttypes.models import ContentType

from extras.plugins import PluginTemplateExtension
from netbox_storage.models import LogicalVolume, StorageConfigurationDrive, \
    TemplateConfigurationDrive, Drive, Partition, LinuxDevice


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
        print(LinuxDevice.objects.all())
        obj = self.context.get("object")

        drives = TemplateConfigurationDrive.objects.values('drive').filter(platform=obj)
        drives_id = []
        lonely_drives = []
        drives_with_partition = []
        partitions = []
        partition_dict = {
        }
        for drive_id in drives:
            print(f"Right Page: {drive_id['drive']}")
            drives_id.append(drive_id['drive'])
            drive = Drive.objects.get(pk=drive_id['drive'])

            drive_type_id = ContentType.objects.get(app_label='netbox_storage', model='drive').pk
            linux_device_type_id = ContentType.objects.get(app_label='netbox_storage', model='linuxdevice').pk
            print(f"{drive_type_id}, {drive_id['drive']}")
            # Get Linux Device of Drive e.g. /dev/sda
            linux_device_drive = LinuxDevice.objects.get(content_type_id=drive_type_id, object_id=drive_id['drive'], type='disk')
            print(f"Count: {linux_device_drive}")
            # Wenn es keine Partition hat zu lonely_drives hinzufügen
            if LinuxDevice.objects.filter(content_type_id=linux_device_type_id, object_id=linux_device_drive.pk,
                                          type='Partition').count() == 0:
                print(f"Right Page Lonely Drive: {drive}")
                lonely_drives.append(drive)
                partition_dict[drive] = None
            else:
                drives_with_partition.append(drive)
                partitions.append(list(LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                                                  object_id=linux_device_drive.pk, type='Partition')))
                partition_dict[drive] = list(LinuxDevice.objects.filter(content_type_id=linux_device_type_id,
                                                                                   object_id=linux_device_drive.pk,
                                                                                   type='Partition'))

        amount_partitions = len(partitions)
        print(f"R Lonely Drives: {lonely_drives}")
        print(f"Amount Partitions: {drives_id}")

        return self.render(
            "netbox_storage/inc/template_drive_box.html",
            extra_context={
                "lonely_drives": lonely_drives,
                "drives": drives_with_partition,
                "partitions": partitions,
                "amount_partitions": amount_partitions,
                "partition_dict": partition_dict
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
