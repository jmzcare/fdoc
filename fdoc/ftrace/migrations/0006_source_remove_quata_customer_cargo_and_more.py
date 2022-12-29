# Generated by Django 4.1.4 on 2022-12-21 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ftrace', '0005_alter_customer_customer_nature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=30)),
                ('sort_index', models.IntegerField(default=0)),
                ('cargo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ftrace.cargo')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ftrace.customer')),
                ('source_sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ftrace.source_sector')),
            ],
        ),
        migrations.RemoveField(
            model_name='quata',
            name='customer_cargo',
        ),
        migrations.DeleteModel(
            name='Customer_cargo',
        ),
        migrations.AddField(
            model_name='quata',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ftrace.source'),
        ),
    ]
