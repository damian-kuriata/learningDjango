from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from catalog.views import user, index, image, upload_image, register, search, add_comment, delete_image, settings, \
    delete_image_multiple, test

urlpatterns = [
    path("", index, name="index"),
    #path("user-details/<username>/", user_details, name="user_details"),
    path("image/<int:image_id>/", image, name="image"),
    path("image/<int:id>/delete", delete_image, name="delete-image"),
    path("delete-image-multiple/", delete_image_multiple, name="delete-image-multiple"),
    path("user/<int:id>/", user, name="user"),
    path("user/<int:id>/settings/", settings, name="settings"),
    path("upload-image/", upload_image, name="upload-image"),
    path("search/<query>", search, name="search"),
    path("image/<int:image_id>/add-comment/", add_comment, name="add-comment"),
    path("test/", test, name="test")
]