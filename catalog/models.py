import os

from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_delete

# Custom method that returns canoncial url to access object in HTTP
from django.utils.translation import gettext_lazy


def user_get_absolute_url(self):
    return reverse_lazy("user", args=[str(self.id)])

User.get_absolute_url = user_get_absolute_url

def file_size_validator(value):
    if value.size > settings.MAX_UPLOAD_SIZE:
        msg = "File too big, the maximum file size is: %(size)s bytes"
        raise ValidationError(msg, params={"size": settings.MAX_UPLOAD_SIZE})

class UploadedImage(models.Model):
    class Meta:
        ordering = ["title"]
        verbose_name = gettext_lazy("uploaded image")
        verbose_name_plural = gettext_lazy("uploaded images")

    title = models.CharField(max_length=30,
                             help_text="Required. Max 30 character title for "
                                       "your image")
    description = models.CharField(max_length=150,
                                   help_text="Required.Max 150 character description "
                                             "of your image")
    def get_upload_path(instance, filename):
        return os.path.join("uploaded_images", str(instance.author_id), filename)

    image = models.ImageField(upload_to=get_upload_path,
                              validators=[file_size_validator],
                              help_text=f"Max. file size: {settings.MAX_UPLOAD_SIZE}")
    upload_datetime = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("image", args=[str(self.id)])

    def __str__(self):
        return self.title


# Receiver which gets triggered when object is being deleted
@receiver(pre_delete, sender=UploadedImage)
def delete_image_file(sender, instance, using, **kwargs):
    try:
        imgpath = instance.image.path
        os.remove(imgpath)
        # Remove directory if empty
        if len(os.listdir(os.path.dirname(imgpath))) == 0:
            os.rmdir(os.path.dirname(imgpath))
    except:
        pass


class Comment(models.Model):
    uploaded_image = models.ForeignKey(UploadedImage,
                                       on_delete=models.CASCADE)
    text = models.TextField(max_length=1000,
                            help_text="Write your comment. 1000 characters max")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def get_absolute_url(self):
        pass
        return reverse_lazy("uploaded-images", args=[str(self.uploaded_image.id)])

    def __str__(self):
        return self.text