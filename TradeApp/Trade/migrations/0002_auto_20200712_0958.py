# Generated by Django 3.0.7 on 2020-07-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trade', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symbol',
            name='name',
            field=models.CharField(max_length=1024, unique=True),
        ),
    ]