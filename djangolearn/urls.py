from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from djangolearn.views import LearnView, ManageLanguagesView, LanguageView

app_name = "djangolearn"
# TODO: fix re_path for learn
urlpatterns = [
    path("index/", TemplateView.as_view(template_name="djangolearn/index.html"), name="index"),
    re_path(r"learn/((?P<language>\w+)/)?$", LearnView.as_view(), name="learn"),
    path("manage-languages/", ManageLanguagesView.as_view(), name="manage-languages"),
    re_path(r"api/languages/((?P<language>\w+)/)?$", csrf_exempt(LanguageView.as_view()), name="language")
]