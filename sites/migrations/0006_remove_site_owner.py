# Generated by Django 5.0.2 on 2024-02-18 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0005_alter_site_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='site',
            name='owner',
        ),
    ]