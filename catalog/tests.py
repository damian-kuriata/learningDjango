import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user("Damianek1", "passwd")
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_index_view(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200

def test_admin(admin_client):
    url = reverse("admin:index")
    response = admin_client.get(url)
    assert response.status_code == 201


def test_user_model(client, django_user_model):
    user = django_user_model.objects.create_user("Damianek111", password="passwd")
    url = reverse("")