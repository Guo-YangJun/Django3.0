# Generated by Django 2.1.5 on 2019-03-21 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=32)),
                ('url', models.TextField()),
            ],
        ),
    ]
