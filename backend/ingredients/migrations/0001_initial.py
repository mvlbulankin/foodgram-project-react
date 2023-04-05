# Generated by Django 4.1.7 on 2023-04-05 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_unit', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
