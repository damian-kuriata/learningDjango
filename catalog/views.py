import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from catalog.forms import UploadedImageForm, RegisterForm
from catalog.models import UploadedImage, Comment


def index(request):
    recently_uploaded_images = \
        UploadedImage.objects.order_by("-upload_datetime")
    objects_per_page = 1
    paginator = Paginator(recently_uploaded_images, objects_per_page)
    page_number = request.GET.get("page")
    try:
        page_number = int(page_number)
    except:
        page_number = None
    if page_number and page_number > 1:
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = paginator.get_page(1)
    return render(request, "catalog/index.html", {
        "images": recently_uploaded_images,
        "page_obj": page_obj
    })

def user(request, id):
    user = get_object_or_404(User, id=id)
    uploaded_images = user.uploadedimage_set.all()

    return render(request, "catalog/user.html",
                  {"images": uploaded_images})

def settings(request, id):
    user = get_object_or_404(User, id=id)
    return render(request, "catalog/settings.html", {"user": user})

@require_http_methods(["DELETE"])
def delete_image(request, id):
    try:
        image = UploadedImage.objects.get(id=id)
    except UploadedImage.DoesNotExist:
        json_ = {"error": f"Image with id {id} does not exist"}
    except UploadedImage.MultipleObjectsReturned:
        json_ = {"error": "Internal server error"}
    else:
        image.delete()
    finally:
        return JsonResponse(json_)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_image_multiple(request):
    deleted_image_ids = request.body.decode("utf-8")
    deleted_image_ids = deleted_image_ids.split(';')
    if not deleted_image_ids:
        return JsonResponse({"error": "No images to delete"})
    for id_ in deleted_image_ids:
        try:
            id_ = int(id_)
        except ValueError:
            return JsonResponse({"error": f"Id {id_} is not a number"})
        try:
            UploadedImage.objects.get(id=id_).delete()
        except UploadedImage.DoesNotExist:
            return JsonResponse({"error": f"Image with id {id_} does not exist"})
        except UploadedImage.MultipleObjectsReturned:
            return JsonResponse({"error": "Internal server error"})
    return JsonResponse({"info": "Deletion sucessfull"})

def image(request, image_id):
    image = get_object_or_404(UploadedImage, pk=image_id)
    return render(request, "catalog/image.html", {"image": image})

def upload_image(request):
    if request.method == "POST":
        form = UploadedImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            user = request.user
            if isinstance(user, AnonymousUser):
                user = User.objects.get(username="AnonymousUser")
            uploaded_image.author = user
            uploaded_image.save()
            messages.info(request, "Image uploaded successfully",
                          extra_tags="message-info")
            return HttpResponseRedirect(reverse("image",
                                                args=[str(uploaded_image.id)]))
        else:
            return render(request, "catalog/upload_image.html", {"form": form})
    else:
        form = UploadedImageForm()
        return render(request, "catalog/upload_image.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.info(request, "You have been successfully registered!",
                          extra_tags="message-success")
            return HttpResponseRedirect(reverse("login"))
        else:
            return render(request, "catalog/register_form.html", {"form": form})
    else:
        form = RegisterForm()
        return render(request, "catalog/register_form.html", {"form": form})


def search(request, query):
    images_title = UploadedImage.objects.filter(title__icontains=query)
    images_desc = UploadedImage.objects.filter(description__icontains=query)
    users = User.objects.filter(username__icontains=query)
    return render(request, "catalog/search.html", {
        "images_title": images_title,
        "images_desc": images_desc,
        "users": users
    })

@require_POST
def add_comment(request, image_id):
    associated_image = get_object_or_404(UploadedImage, pk=image_id)
    user = request.user
    if isinstance(user, AnonymousUser):
        user = User.objects.get(username="AnonymousUser")
    written_comment_json = json.loads(request.body.decode("utf-8"))
    written_comment = Comment(text=written_comment_json["comment"])
    written_comment.author = user
    written_comment.uploaded_image = associated_image
    written_comment.save()
    return JsonResponse({"username": user.username, "absolute_url": user.get_absolute_url()})

@csrf_exempt
def test(request):
    response = HttpResponse("text")
    print("test")
    return response