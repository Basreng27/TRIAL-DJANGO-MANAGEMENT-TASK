# Generated by Django 5.0.8 on 2024-08-30 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackendRest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileattachments',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to='ManagementTask/public/files/'),
        ),
    ]
