from django.db import models
from ..base.validators import validate_image_size


class AboutUs(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name="متن درباره ما")
    image1 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 1 درباره ما",
                               validators=[validate_image_size])
    image2 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 2 درباره ما",
                               validators=[validate_image_size])
    image3 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 3 درباره ما",
                               validators=[validate_image_size])
    video = models.CharField(max_length=150, null=True, blank=True, verbose_name="لینک ویدیو")

    gallery1 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 1 گالری",
                                 validators=[validate_image_size])
    gallery2 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 2 گالری",
                                 validators=[validate_image_size])
    gallery3 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 3 گالری",
                                 validators=[validate_image_size])
    gallery4 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 4 گالری",
                                 validators=[validate_image_size])
    gallery5 = models.ImageField(upload_to="setting/", null=True, blank=True, verbose_name=" تصویر 5 گالری",
                                 validators=[validate_image_size])

    class Meta:
        verbose_name = ("تنظیمات درباره ما")
        verbose_name_plural = ("تنظیمات درباره ما")

    def __str__(self):
        return "تنظیمات درباره ما"
