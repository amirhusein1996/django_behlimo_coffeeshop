from django.conf import settings
from django.core.exceptions import ValidationError


# limit size image and raise error
def validate_image_size(value):
    limit = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
    if value.size > limit:
        raise ValidationError(f'حجم فایل بیشتر از {limit / 1024 / 1024:.2f} MB است')