# Generated by Django 2.1.5 on 2019-03-04 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankcard',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='types',
            name='parent_id',
        ),
        migrations.DeleteModel(
            name='BankCard',
        ),
    ]
