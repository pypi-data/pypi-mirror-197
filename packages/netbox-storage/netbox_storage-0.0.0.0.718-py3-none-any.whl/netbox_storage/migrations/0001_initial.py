from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
import utilities.json


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="Filesystem",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("filesystem", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("filesystem", "id"),
            },
        ),
        migrations.CreateModel(
            name="Drive",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("cluster",
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="cluster_drive",
                                   to="virtualization.cluster")),
                ("size", models.FloatField()),
                ("identifier", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("size", "id"),
            },
        ),
        migrations.CreateModel(
            name="MountedVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("mount_point", models.CharField(max_length=255)),
                ("fs_type",
                 models.ForeignKey(blank=True,
                                   null=True,
                                   on_delete=models.deletion.CASCADE,
                                   related_name='fs_mounted_volume',
                                   to='netbox_storage.filesystem')),
                ("options", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("mount_point", "fs_type", "options"),
            },
        ),
        migrations.CreateModel(
            name="LinuxDevice",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("device", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("size", models.FloatField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type',
                 models.ForeignKey(on_delete=models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name="Partition",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("drive",
                 models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="drive_partition",
                                   to="netbox_storage.drive")),
                ("device", models.ForeignKey(on_delete=models.deletion.PROTECT, related_name="device_partition",
                                             to='netbox_storage.linuxdevice')),
                ("size", models.FloatField()),
                ("type", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("size", "id"),
            },
        ),
        migrations.CreateModel(
            name="VolumeGroup",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vg_name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("vg_name", "id"),
            },
        ),
        migrations.CreateModel(
            name="PhysicalVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("device",
                 models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="device_physicalvolume",
                                      to="netbox_storage.partition")),
                ("vg",
                 models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="volumegroup_physicalvolume",
                                   to="netbox_storage.volumegroup", null=True)),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("device", "vg"),
            },
        ),
        migrations.CreateModel(
            name="LogicalVolume",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vg", models.ForeignKey(on_delete=models.deletion.CASCADE,
                                         related_name="volumegroup_logicalvolume",
                                         to="netbox_storage.volumegroup")),
                ("lv_name", models.CharField(max_length=255)),
                ("size", models.FloatField()),
                ('device', models.ForeignKey(on_delete=models.deletion.CASCADE,
                                             related_name="device_logical_volume",
                                             to="netbox_storage.linuxdevice")),
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("lv_name", "id"),
            },
        ),
        migrations.CreateModel(
            name="StorageConfigurationDrive",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("virtual_machine",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name="virtual_machine_storage_configuration",
                                   to="virtualization.virtualmachine")),
                ("drive",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name='drive_storage_configuration',
                                   to='netbox_storage.drive')),
            ],
        ),
        migrations.CreateModel(
            name="TemplateConfigurationDrive",
            fields=[
                ("created", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "custom_field_data",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=utilities.json.CustomFieldJSONEncoder
                    ),
                ),
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("platform",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name="platform_template_configuration",
                                   to="dcim.platform")),
                ("drive",
                 models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE,
                                   related_name='drive_template_configuration',
                                   to='netbox_storage.drive')),
            ],
        ),
    ]
