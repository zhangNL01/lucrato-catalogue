# Generated by Django 4.0.4 on 2022-06-20 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_catalogueuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='seller_info',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
