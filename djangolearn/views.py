import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from djangolearn.forms import LanguageSelectForm
from djangolearn.models import Language


class LearnView(LoginRequiredMixin, View):
    form_class = LanguageSelectForm
    template_name = "djangolearn/language_select_form.html"

    def get(self, request, *args, **kwargs):
        language_to_learn = kwargs.get("language", '')
        language_to_learn = language_to_learn.lower()
        if not language_to_learn or \
            language_to_learn not in settings.LANG_CHOICES[0]:
            # If no language is selected or language is wrong, (re)display form
            form = self.form_class()
            return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            learn_arg = form.cleaned_data["language"]
            print(learn_arg)
            # TODO: write this method
            return HttpResponseRedirect(reverse("djangolearn:learn"))


class ManageLanguagesView(LoginRequiredMixin, View):
    template_name = "djangolearn/manage_languages.html"

    def get(self, request, *args, **kwargs):
        user_languages = request.user.language_set.all().order_by("name")
        return render(request, self.template_name,
                      {"user_languages": user_languages})

# --- API ---
class LanguageView(View):
    # TODO: Implement credentials checking
    def check_user_credentials(self, request_json):
        try:
            request_dict = json.loads(request_json)
            username = request_dict.get("username")
            password = request_dict.get("password")
            user = User.objects.filter(username__iexact=username).first()
            if user and user.check_password(password) and user.is_active():
                return True
            else:
                return JsonResponse({"error": "Unauthorized"}, status=401)
        except json.JSONDecodeError as err:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    def get(self, request, *args, **kwargs):
        language_name = kwargs.get("language")
        language = Language.objects.filter(name__iexact=language_name).first()
        fields = ("pk", "name", "user", "phrase_set")
        if language:
            iterable = [language]
        else:
            iterable = Language.objects.all()
        json_ = serializers.serialize("json", iterable, fields=fields)
        return JsonResponse(json_, safe=False)

    def post(self, request, *args, **kwargs):
        try:
            language_name = kwargs.get("language")
            if Language.objects.filter(name__iexact=language_name).exists():
                return JsonResponse({"error": f"Language named {language_name} exists"})

            else:
                user = request.user
                language = Language(name=language_name)
                language.user = user
                language.save()
                return JsonResponse({"success":
                                         f"Language {language_name} created"})
        except json.JSONDecodeError as err:
            return JsonResponse({"error": err.msg}, status=400)

    def delete(self, request, *args, **kwargs):
        language_name = kwargs.get("language")
        language = Language.objects.filter(name__iexact=language_name).first()
        if language:
            language.delete()
            return JsonResponse({"success": f"Language {language_name} deleted"})
        else:
            return JsonResponse({"error": f"Language {language_name} not found"})


class DeleteLanguageView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        language_name = kwargs.get("language")
        try:
            language = Language.objects.get(name__iexact=language_name)
            language.delete()
            return JsonResponse({"success": f"Language {language_name} deleted"})
        except Language.DoesNotExist:
            response = {"error": f"Language named {language_name} "
                                 f"does not exist"}
            return JsonResponse(response)
        except Language.MultipleObjectsReturned:
            response = {"error": f"Multiple languages named "
                                 f"{language_name} found"}
            return JsonResponse(response)


class AddLanguageView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            language_name = json.loads(request.body)["language_name"]
            if Language.objects.filter(language_name).exists():
                reason = {"error": f"Language named {language_name} "
                                   f"already exists"}
                return JsonResponse(reason)
            language = Language(name=language_name)
            language.user = request.user
            language.save()
            reason = {"success": f"Language named {language_name} created!"}
            return JsonResponse(reason)
        except json.JSONDecodeError as err:
            return JsonResponse({"error": err.msg})




