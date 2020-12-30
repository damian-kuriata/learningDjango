from django.contrib import admin
from catalog.models import UploadedImage, Comment


class UploadedImageAdmin(admin.ModelAdmin):
    date_hierarchy = "upload_datetime"

class CommentAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Comment, CommentAdmin)
#admin.site.register(UploadedImage, UploadedImageAdmin)