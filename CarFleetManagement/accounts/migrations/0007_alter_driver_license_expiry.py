
from django.db import migrations, models

"""Migration file."""

class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_userrole_name"),
    ]

    operations = [
        # The field did not exist in the original create migration (0005_driver).
        # Use AddField to create the column with the nullable/blank properties.
        migrations.AddField(
            model_name="driver",
            name="license_expiry_date",
            field=models.DateField(null=True, blank=True),
        ),
    ]
