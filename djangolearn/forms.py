from django.forms import ModelForm, Textarea, NumberInput

from djangolearn.models import Language, Phrase


class LanguageForm(ModelForm):
    class Meta:
        model = Language
        fields = ("name",)


class PhraseForm(ModelForm):
    class Meta:
        model = Phrase
        fields = ("non_translated_text", "translated_text", "language",
                  "priority", "image")
        widgets = {
            "non_translated_text": Textarea(attrs={"cols": 15, "rows": 6}),
            "translated_text": Textarea(attrs={"cols": 15, "rows": 6}),
            "priority": NumberInput(attrs={"max": "10", "min": "0"})
        }

