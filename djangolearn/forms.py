from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from djangolearn.models import Language, Phrase


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ("name",)


class PhraseForm(forms.ModelForm):
    class Meta:
        model = Phrase
        fields = ("non_translated_text", "translated_text", "language",
                  "priority", "image")
        widgets = {
            "non_translated_text": forms.Textarea(attrs={"cols": 15, "rows": 6}),
            "translated_text": forms.Textarea(attrs={"cols": 15, "rows": 6}),
            "priority": forms.NumberInput(attrs={"max": "10", "min": "0"})
        }

class LanguageSelectForm(forms.Form):
    language = forms.ChoiceField(label=_("Select language to learn"),
                                 choices=settings.LANG_CHOICES)