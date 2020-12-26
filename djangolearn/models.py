import re
import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator

# TODO: Do filename checking.
def get_upload_path(instance, filename):
    return os.path.join("phrase_images", instance.user.id, filename)


class Language(models.Model):
    # TODO: Restrict language name to predefined choices list.
    name = models.CharField(max_length=20,
                            validators=[RegexValidator("^[A-Z ]+$",
                                        flags=re.I)])

    class Meta:
        ordering = ["name"]
        verbose_name = _("language")
        verbose_name_plural = _("languages")


class Phrase(models.Model):
    non_translated_text = models.TextField(_("non_translated_text"))
    translated_text = models.TextField(_("translated_text"))
    language = models.ForeignKey(Language, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    # Number in range 0 to 10 indicating possibility of this phrase being selected
    priority = models.IntegerField(_("priority"), validators=[
        MinValueValidator(0), MaxValueValidator(10)])
    image = models.ImageField(_("image"), upload_to=get_upload_path, blank=True)

    class Meta:
        ordering = ["language"]
        verbose_name = _("phrase")
        verbose_name_plural = _("phrases")


@receiver(pre_delete, sender=Phrase)
def delete_image_file(sender, instance, using, **kwargs):
    try:
        imgpath = instance.image.path
        os.remove(imgpath)
        # Remove directory if empty
        if len(os.listdir(os.path.dirname(imgpath))) == 0:
            os.rmdir(os.path.dirname(imgpath))
    except:
        pass
