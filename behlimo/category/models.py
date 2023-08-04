from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from ..base.validators import validate_image_size


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.CharField(unique=True, max_length=255, verbose_name='نام کوتاه')
    image = models.ImageField(upload_to='media/', verbose_name='تصویر دسته بندی', validators=[validate_image_size])
    description = models.TextField(verbose_name='توضیحات دسته بندی')

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def get_url(self):
        return reverse('menu_by_category', args=[self.slug])

    def image_tag(self):
        return format_html('<img src="{}" width="50" height="50" />'.format(self.image.url))

    image_tag.short_description = 'تصویر'

    def __str__(self):
        return self.title
