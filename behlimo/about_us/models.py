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
    is_enabled = models.BooleanField(verbose_name='enabled', default=False)

    class Meta:
        verbose_name = ("تنظیمات درباره ما")
        verbose_name_plural = ("تنظیمات درباره ما")

    def __str__(self):
        return "تنظیمات درباره ما"
    
    def save(self, *args, **kwargs):

        """
        Override the save method.

        If this object is enabled, disable all other enabled AboutUs
        objects, except for this object itself. This ensures there
        is only one enabled AboutUs object.

        Then call the super save method to actually save this object.
        """

        if self.is_enabled:
            AboutUs.objects.filter(
                is_enabled=True
            ).exclude(
                id=self.id
            ).update(
                is_enabled=False
            )
        super().save(*args, **kwargs)
