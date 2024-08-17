# Generated by Django 4.2.5 on 2024-08-15 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_medium_height_medium_width'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='workpiece',
            name='worker',
        ),
        migrations.AddIndex(
            model_name='worker',
            index=models.Index(fields=['last_name'], name='api_worker_last_na_7cc911_idx'),
        ),
        migrations.AddIndex(
            model_name='worker',
            index=models.Index(fields=['first_name'], name='api_worker_first_n_b81852_idx'),
        ),
        migrations.AddIndex(
            model_name='worker',
            index=models.Index(fields=['ymd_birth'], name='api_worker_ymd_bir_df3925_idx'),
        ),
        migrations.AddIndex(
            model_name='workinterval',
            index=models.Index(fields=['start_utcms'], name='api_workint_start_u_278d3c_idx'),
        ),
        migrations.AddIndex(
            model_name='workpiece',
            index=models.Index(fields=['start'], name='api_workpie_start_bd1d74_idx'),
        ),
        migrations.AddIndex(
            model_name='worktype',
            index=models.Index(fields=['name'], name='api_worktyp_name_906619_idx'),
        ),
        migrations.AddField(
            model_name='workpiece',
            name='worker',
            field=models.ManyToManyField(to='api.worker'),
        ),
    ]