# Generated by Django 2.2.17 on 2021-03-23 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('readingTime', '0013_auto_20210323_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readingTime.Category'),
        ),
    ]
