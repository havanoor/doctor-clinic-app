# Generated by Django 3.0.7 on 2020-07-27 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.TextField(),
        ),
    ]
