# Generated by Django 4.2.5 on 2024-08-18 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_workinterval_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='finished',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='started',
            field=models.DateTimeField(null=True),
        ),
    ]