from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_userrole_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="driver",
            name="license_expiry_date",
            field=models.DateField(null=True, blank=True),
        ),
    ]
