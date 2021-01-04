import re
import os

from django.conf import settings
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
    name = models.CharField(_("name"), max_length=20,
                            validators=[RegexValidator("^[A-Z ]+$",
                                        flags=re.I)],
                            choices=settings.LANG_CHOICES)
    user = models.ForeignKey(User, models.CASCADE)

    class Meta:
        ordering = ["name"]
        verbose_name = _("language")
        verbose_name_plural = _("languages")

    def check_phrase(self, phrase, translated_phrase, translation_direction):
        """
        Check if phrase is correct

        :param phrase: Phrase object
        :param translated_phrase: string: a phrase translated by user
        :param translation_direction: 'to_foreign' or 'from_foreign'
        :return: bool, depending on the phrase is correct or not
        """

        original_phrase = phrase.translated_text.strip().lower()
        translated_phrase = translated_phrase.strip().lower()

        # Replace 2 or more spaces with only one space
        original_phrase = re.sub(r" {2,}", " ", original_phrase)
        translated_phrase = re.sub(r" {2,}", " ", translated_phrase)
        # Remove all newline characters (e.g. replace them with empty string)
        original_phrase = original_phrase.replace("\n", "")
        translated_phrase = translated_phrase.replace("\n", "")

        translation_direction = translation_direction.strip().lower()
        # TODO: Implement actual checking
        print("check original", original_phrase)
        print("check translated", translated_phrase)
        print("check type", original_phrase == translated_phrase)
        return original_phrase == translated_phrase
        if self.name == settings.LANG_ENGLISH:
            pass

    # TODO: implement 'get_absolute_url' method
    def __str__(self):
        return self.name


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
    def __str__(self):
        return self.non_translated_text[:20]


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
