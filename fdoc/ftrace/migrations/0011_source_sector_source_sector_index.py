# Generated by Django 4.1.4 on 2022-12-24 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ftrace', '0010_alter_booker_booker_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='source_sector',
            name='source_sector_index',
            field=models.IntegerField(default=0),
        ),
    ]
