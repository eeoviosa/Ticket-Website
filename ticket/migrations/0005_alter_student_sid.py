# Generated by Django 4.1.7 on 2023-04-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket", "0004_rename_studentid_student_sid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="sid",
            field=models.IntegerField(default=123456, max_length=7),
        ),
    ]
