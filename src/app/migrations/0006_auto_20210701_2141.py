# Generated by Django 3.1.12 on 2021-07-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210626_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='receipt',
            field=models.ImageField(blank=True, null=True, upload_to='receipts\\'),
        ),
    ]
