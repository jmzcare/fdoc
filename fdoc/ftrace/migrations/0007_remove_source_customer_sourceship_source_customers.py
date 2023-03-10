# Generated by Django 4.1.4 on 2022-12-21 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ftrace', '0006_source_remove_quata_customer_cargo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='customer',
        ),
        migrations.CreateModel(
            name='Sourceship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftrace.customer')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ftrace.source')),
            ],
        ),
        migrations.AddField(
            model_name='source',
            name='customers',
            field=models.ManyToManyField(through='ftrace.Sourceship', to='ftrace.customer'),
        ),
    ]
