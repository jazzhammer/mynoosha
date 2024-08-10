# Generated by Django 4.2.5 on 2024-08-10 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_workinterval_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientbillabletype',
            name='agreement',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='api.agreement'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worktype',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
