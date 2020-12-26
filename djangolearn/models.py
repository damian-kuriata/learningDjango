import re
import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator


def get_upload_path(instance, filename):
    return os.path.join("phrase_images", str(instance.user.id), filename)

# Todo implement 'get_absolute_url' for 'User' class


class Language(models.Model):
    LANG_ENGLISH = "en"
    LANG_GERMAN = "de"
    LANG_FRENCH = "fr"
    LANG_SPANISH = "es"
    LANG_POLISH = "pl"
    LANG_CHOICES = (
        (LANG_ENGLISH, _("English")),
        (LANG_GERMAN, _("German")),
        (LANG_FRENCH, _("French")),
        (LANG_SPANISH, _("Spanish")),
        (LANG_POLISH, _("Polish"))
    )
    name = models.CharField(_("name"), max_length=20,
                            validators=[RegexValidator("^[A-Z ]+$",
                                        flags=re.I)],
                            choices=LANG_CHOICES)

    class Meta:
        ordering = ["name"]
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    # TODO: implement 'get_absolute_url' method


class Phrase(models.Model):
    non_translated_text = models.TextField(_("non_translated_text"),
                                           help_text=_("Text you will translate"))
    translated_text = models.TextField(_("translated_text"))
    language = models.ForeignKey(Language, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE, related_name=_("user"),
                             help_text=_("User who added a language"))
    # Number in range 0 to 10 indicating possibility of this phrase being selected
    priority = models.IntegerField(_("priority"), validators=[
        MinValueValidator(0), MaxValueValidator(10)], help_text=_("Number in range"
                                                                " 0 to 10 "
                                                                "indicating "
                                                                "possibility of "
                                                                "this phrase "
                                                                "being selected"))
    image = models.ImageField(_("image"), upload_to=get_upload_path, blank=True,
                              help_text=_("[optional] Image you associated "
                                          "with phrase"))

    class Meta:
        ordering = ["language"]
        verbose_name = _("phrase")
        verbose_name_plural = _("phrases")
    # Todo: implement 'get_absolute_url' method


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
