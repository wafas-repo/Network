# Generated by Django 4.1.4 on 2022-12-12 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
