# Generated by Django 5.1.7 on 2025-04-11 17:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("vehicles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Maintenance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "maintenance_type",
                    models.CharField(
                        choices=[
                            ("ROUTINE", "Routine Maintenance"),
                            ("REPAIR", "Repair"),
                            ("INSPECTION", "Inspection"),
                            ("OTHER", "Other"),
                        ],
                        default="ROUTINE",
                        max_length=15,
                        verbose_name="Maintenance Type",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("SCHEDULED", "Scheduled"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="SCHEDULED",
                        max_length=15,
                        verbose_name="Maintenance Status",
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="Maintenance Description"),
                ),
                ("scheduled_date", models.DateField(verbose_name="Scheduled Date")),
                (
                    "completed_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Completed Date"
                    ),
                ),
                (
                    "odometer_reading",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Odometer Reading",
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Maintenance Cost",
                    ),
                ),
                (
                    "service_provider",
                    models.CharField(max_length=100, verbose_name="Service Provider"),
                ),
                (
                    "notes",
                    models.TextField(blank=True, verbose_name="Additional Notes"),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="maintenance_records",
                        to="vehicles.vehicle",
                        verbose_name="Vehicle",
                    ),
                ),
            ],
        ),
    ]
