# Generated by Django 2.2.17 on 2021-03-22 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('readingTime', '0004_auto_20210322_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='readingTime.Category'),
        ),
    ]
