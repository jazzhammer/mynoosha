# Generated by Django 4.2.5 on 2024-08-12 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_medium_filename_alter_medium_name_alter_medium_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='medium',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='medium',
            name='width',
            field=models.IntegerField(null=True),
        ),
    ]