# Generated by Django 3.2.4 on 2021-07-04 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ping', '0012_alter_url_match_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='match_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
