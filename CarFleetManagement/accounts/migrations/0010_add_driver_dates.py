from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0009_add_driver_status"),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='hire_date',
            field=models.DateField(null=True, blank=True, verbose_name='Hire Date'),
        ),
        migrations.AddField(
            model_name='driver',
            name='termination_date',
            field=models.DateField(null=True, blank=True, verbose_name='Termination Date'),
        ),
    ]
