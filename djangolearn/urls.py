from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
app_name = "djangolearn"
urlpatterns = [
    path("index/", TemplateView.as_view(template_name="djangolearn/index.html"), name="index")
]