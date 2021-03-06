# Generated by Django 2.1.5 on 2019-03-28 22:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)])),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='categori',
            name='dishes',
            field=models.ManyToManyField(to='addDish.Dish'),
        ),
    ]
