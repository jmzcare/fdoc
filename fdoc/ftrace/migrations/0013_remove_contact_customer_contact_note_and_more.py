# Generated by Django 4.1.4 on 2022-12-24 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ftrace', '0012_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='customer',
        ),
        migrations.AddField(
            model_name='contact',
            name='note',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='contact',
            name='sourceship',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ftrace.sourceship'),
        ),
    ]
