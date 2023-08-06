from extras.plugins import PluginTemplateExtension
from netbox_storage.models import LogicalVolume, StorageConfigurationDrive, \
    TemplateConfigurationDrive, Drive, Partition


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

    def full_width_page(self):
        obj = self.context.get("object")

        drives = TemplateConfigurationDrive.objects.values('drive').filter(platform=obj)
        drives_id = []
        lonely_drive = []
        for drive_id in drives:
            print(drive_id['drive'])
            drives_id.append(drive_id['drive'])
            if Partition.objects.filter(drive_id=drive_id['drive']).count() == 0:
                drive = Drive.objects.get(pk=drive_id['drive'])
                print(f"Lonely Drive: {drive}")
                lonely_drive.append(drive)

        partitions = Partition.objects.filter(drive_id__in=drives_id)
        print(f"Lonely Drives: {lonely_drive}")
        print(f"Partitions: {partitions}")
        print(f"drives: {drives_id}")

        return self.render(
            "netbox_storage/inc/template_box.html",
            extra_context={
                "lonely_drives": lonely_drive,
                "partitions": partitions,
            }
        )


template_extensions = [RelatedDrives, TemplateVolumeConfig]
