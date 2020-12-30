from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from djangolearn.views import LearnView

app_name = "djangolearn"
# TODO: fix re_path for learn
urlpatterns = [
    path("index/", TemplateView.as_view(template_name="djangolearn/index.html"), name="index"),
    re_path(r"learn/((?P<language>\w+)/)?$", LearnView.as_view(), name="learn")
]