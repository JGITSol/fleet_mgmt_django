from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_alter_driver_license_expiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userrole",
            name="name",
            field=models.CharField(choices=[
                ("admin", "Admin"),
                ("manager", "Manager"),
                ("coordinator", "Coordinator"),
                ("driver", "Driver"),
                ("testuser", "Test User"),
                ("maintenance_staff", "Maintenance Staff"),
            ], max_length=32),
        ),
    ]
