# Generated by Django 4.1.7 on 2023-05-05 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0006_alter_student_sid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Multi_User",
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
                ("destination", models.CharField(max_length=100)),
                ("file_name", models.CharField(max_length=100)),
            ],
        ),
    ]
