from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from djangolearn.forms import LanguageSelectForm


class LearnView(LoginRequiredMixin, View):
    form_class = LanguageSelectForm
    template_name = "djangolearn/language_select_form.html"
    def get(self, request, *args, **kwargs):
        language_to_learn = kwargs.get("language", '')
        language_to_learn = language_to_learn.lower()
        user_languages = 1
        if not language_to_learn or \
            language_to_learn not in settings.LANG_CHOICES[0]:
            # If no language is selected or language is wrong, (re)display form
            form = self.form_class()
            return render(request, self.template_name, {"form": form})
