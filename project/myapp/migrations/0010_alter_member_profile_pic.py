# Generated by Django 5.0.1 on 2024-08-27 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_member_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_pics/logo.png', null=True, upload_to='profile_pics/'),
        ),
    ]
