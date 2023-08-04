# Generated by Django 3.1 on 2023-04-29 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='متن درباره ما')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 1 درباره ما')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 2 درباره ما')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 3 درباره ما')),
                ('video', models.CharField(blank=True, max_length=150, null=True, verbose_name='لینک ویدیو')),
                ('gallery1', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 1 گالری')),
                ('gallery2', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 2 گالری')),
                ('gallery3', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 3 گالری')),
                ('gallery4', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 4 گالری')),
                ('gallery5', models.ImageField(blank=True, null=True, upload_to='setting/', verbose_name=' تصویر 5 گالری')),
            ],
            options={
                'verbose_name': 'تنظیمات درباره ما',
                'verbose_name_plural': 'تنظیمات درباره ما',
            },
        ),
    ]