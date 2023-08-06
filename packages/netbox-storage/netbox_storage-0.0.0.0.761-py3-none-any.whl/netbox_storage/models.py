from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum, CharField
from django.urls import reverse

from netbox.models import NetBoxModel
from netbox_storage.choices import OSTypeChoices


class Filesystem(NetBoxModel):
    filesystem = models.CharField(
        unique=True,
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ['filesystem', 'description']

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:filesystem', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.filesystem}'

    class Meta:
        ordering = ('filesystem', 'description')


class Drive(NetBoxModel):
    cluster = models.ForeignKey(
        to='virtualization.Cluster',
        on_delete=models.PROTECT,
        related_name='cluster_drive',
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    identifier = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ['cluster', 'size', 'identifier', 'description']

    prerequisite_models = (
        'virtualization.Cluster',
    )

    class Meta:
        ordering = ['size']

    def __str__(self):
        return f'{self.identifier} ({self.size} MB {self.cluster})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:drive', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        is_already_implemented = Drive.objects.filter(id=self.pk).count()
        if is_already_implemented == 0:
            number_of_hard_drives = Drive.objects.all().\
                order_by('created').count()

            self.identifier = f'Hard Drive {number_of_hard_drives + 1}'

        super(Drive, self).save(*args, **kwargs)

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/drive/'

    def partition_count(self):
        return Partition.objects.filter(drive=self).count()

    def device_name(self):
        return f'/dev/sd{chr(ord("`") + int(self.identifier[-1]))}'

    def physicalvolumes_in_drive_count(self):
        return PhysicalVolume.objects.filter(drive=self).count()

    def left_free_space(self):
        current_partition_allocated_space = Partition.objects.filter(drive=self).aggregate(sum=Sum('size')).get(
            'sum') or 0
        return self.size - current_partition_allocated_space


class LinuxDevice(NetBoxModel):
    device = models.CharField(
        max_length=255,
    )
    type = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveBigIntegerField()
    object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_id'
    )

    clone_fields = ['device', 'type', 'size', 'content_type', 'object_id']

    class Meta:
        ordering = ['device', 'type', 'size', 'content_type', 'object_id']

    def __str__(self):
        return f'{self.device} ({self.type})'

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:linuxdevice', kwargs={'pk': self.pk})


class Partition(NetBoxModel):
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_partition',
    )
    device = models.ForeignKey(
        LinuxDevice,
        on_delete=models.CASCADE,
        related_name='device_partition',
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    type = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = ['drive', 'device', 'size', 'type', 'description']

    prerequisite_models = (
        'netbox_storage.Drive',
    )

    class Meta:
        ordering = ['size']

    def __str__(self):
        return f'{self.device}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:partition', kwargs={'pk': self.pk})

    @property
    def docs_url(self):
        return f'https://confluence.ti8m.ch/docs/models/partition/'

    '''def clean(self, *args, **kwargs):
        total_allocated_space = Partition.objects.filter(drive=self.drive).aggregate(sum=Sum('size')).get('sum') or 0
        current_partition_size = Partition.objects.filter(drive=self.drive, id=self.pk) \
                                     .aggregate(sum=Sum('size')).get('sum') or 0
        if self.size is None:
            raise ValidationError(
                {
                    'size': f'The Value for Size must be greater than 0'
                }
            )
        diff_to_allocated_space = self.size - current_partition_size
        if diff_to_allocated_space > 0:
            if total_allocated_space == self.drive.size:
                raise ValidationError(
                    {
                        'size': f'The maximum Space of the hard drive was already allocated.'
                    }
                )
            if self.size > self.drive.size:
                raise ValidationError(
                    {
                        'size': f'The size of the Partition is bigger than the size of the Hard Drive.'
                    }
                )
            if total_allocated_space + self.size > self.drive.size:
                raise ValidationError(
                    {
                        'size': f'The size of the Partition is bigger than the size of the Hard Drive.'
                    }
                )
'''
    def get_affiliated_physical_volume(self):
        return PhysicalVolume.objects.filter(partition=self).first()


class VolumeGroup(NetBoxModel):
    vg_name = models.CharField(
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'vg_name',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:volumegroup', kwargs={'pk': self.pk})

    def __str__(self):
        return self.vg_name

    class Meta:
        ordering = ('vg_name', 'description')

    def physical_volume_count(self):
        return PhysicalVolume.objects.filter(vg=self).count()

    def logical_volume_count(self):
        return LogicalVolume.objects.filter(vg=self).count()

    def get_total_affiliated_size(self):
        total_sum = 0
        for PV in PhysicalVolume.objects.filter(vg=self):
            total_sum += PV.partition.size
        return total_sum


class PhysicalVolume(NetBoxModel):
    linux_device = models.ForeignKey(
        LinuxDevice,
        on_delete=models.CASCADE,
        related_name='linux_device_physicalvolume',
    )
    vg = models.ForeignKey(
        VolumeGroup,
        on_delete=models.CASCADE,
        related_name='volumegroup_physicalvolume',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'linux_device',
        'vg',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:physicalvolume', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.linux_device}'

    class Meta:
        ordering = ('linux_device', 'description')


class LogicalVolume(NetBoxModel):
    vg = models.ForeignKey(VolumeGroup, on_delete=models.CASCADE, related_name='volumegroup_logicalvolume')
    lv_name = models.CharField(
        max_length=255,
    )
    size = models.FloatField(
        verbose_name='Size (GB)'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'vg',
        'lv_name',
        'size',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:logicalvolume', kwargs={'pk': self.pk})

    def __str__(self):
        return self.lv_name

    class Meta:
        ordering = ('lv_name', 'description')


class StorageConfigurationDrive(NetBoxModel):
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='virtual_machine_storage_configuration',
    )
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_storage_configuration'
    )

    clone_fields = [
        'virtual_machine',
        'drive',
    ]

    class Meta:
        ordering = ['virtual_machine', 'drive']

    def __str__(self):
        return f'Storage Configuration of the VM {self.virtual_machine}'


class TemplateConfigurationDrive(NetBoxModel):
    platform = models.ForeignKey(
        to='dcim.platform',
        on_delete=models.CASCADE,
        related_name='platform_template_configuration',
    )
    drive = models.ForeignKey(
        Drive,
        on_delete=models.CASCADE,
        related_name='drive_template_configuration'
    )

    clone_fields = [
        'platform',
        'drive',
    ]

    class Meta:
        ordering = ['platform', 'drive']

    # def get_absolute_url(self):
    #     return reverse('plugins:netbox_storage:storageconfiguration', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Template Configuration of the Platform {self.platform}'


class MountedVolume(NetBoxModel):
    linux_device = models.ForeignKey(
        LinuxDevice,
        on_delete=models.CASCADE,
        related_name='linux_device_mounted_volume',
    )
    mount_point = models.CharField(
        max_length=255,
    )
    fs_type = models.ForeignKey(
        Filesystem,
        on_delete=models.CASCADE,
        related_name='fs_mounted_volume',
        verbose_name='Filesystem',
    )
    options = models.CharField(
        max_length=255,
        blank=True,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )

    clone_fields = [
        'linux_device',
        'mount_point',
        'fs_type',
        'options',
        'description',
    ]

    def get_absolute_url(self):
        return reverse('plugins:netbox_storage:mountedvolume', kwargs={'pk': self.pk})

    def __str__(self):
        return f'Filesystem Table Entry: mounted to {self.mount_point}'

    class Meta:
        ordering = ('linux_device', 'mount_point', 'fs_type', 'options', 'description')
