# Generated by Django 4.2.5 on 2024-08-18 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_project_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='workinterval',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.project'),
        ),
    ]
