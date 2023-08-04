# Generated by Django 3.1 on 2023-04-16 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name=' نام و نام خانوادگی')),
                ('phone_number', models.CharField(max_length=20, verbose_name='شماره تلفن')),
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'باشگاه مشتریان',
            },
        ),
    ]