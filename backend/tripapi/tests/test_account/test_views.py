from typing import TypeVar

import pytest
from account.models import User
from django.test.client import Client
from rest_framework import status
from rest_framework.reverse import reverse
from utils.base.errors import ApiResponse

T = TypeVar('T', bound=Client)


pytestmark = pytest.mark.django_db


def login_user(admin_api_key_headers, client: T):
    url = reverse('auth:login')
    data = {
        'email': 'test_email@gmail.com',
        'password': 'randopass'
    }
    response = client.post(
        url, data, format='json',
        **admin_api_key_headers)

    return response.data.get('tokens', '')


@pytest.mark.usefixtures('basic_user', 'admin_user')
def test_user_count():
    user_count = User.objects.count()
    assert user_count == 2


def test_user_login_api_permissions(client: T):
    url = reverse('auth:login')
    data = {}
    response = client.post(
        url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures('basic_user')
def test_user_login(client: T, admin_api_key_headers, basic_user_data):
    url = reverse('auth:login')
    response = client.post(
        url, basic_user_data, format='json',
        **admin_api_key_headers
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()['data']
    tokens = response_data['tokens']
    user = response_data['user']
    assert bool(tokens) is True
    assert bool(user) is True
    assert bool(tokens['refresh']) is True
    assert bool(tokens['access']) is True


@pytest.mark.usefixtures('basic_user')
def test_user_login_unverified_email(
    client: T, admin_api_key_headers, basic_user_data, basic_user
):
    basic_user.verified_email = False
    basic_user.save()
    url = reverse('auth:login')
    response = client.post(
        url, basic_user_data, format='json',
        **admin_api_key_headers
    )
    assert response.status_code == 400
    response_data = response.json()['data']
    code = response_data['code']
    assert code == ApiResponse.EMAIL_NOT_VERIFIED.code


def test_user_registration_permission(client: T):
    url = reverse('auth:register')
    response = client.post(url, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    'name, value',
    [
        ('email', 'sketcherslodge'),
        ('first_name', 'Netrobe000000000000000000000000'),
        ('last_name', 'webby;d8$'),
        ('password', '1234'),
    ]
)
def test_user_registration_wrong_data(
    client: T, user_create_data: dict, admin_api_key_headers,
    name, value
):
    url = reverse('auth:register')
    user_create_data[name] = value
    response = client.post(
        url, user_create_data, format='json', **admin_api_key_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_user_registration_success(
    client: T, user_create_data: dict, admin_api_key_headers
):
    url = reverse('auth:register')
    response = client.post(
        url, user_create_data, format='json', **admin_api_key_headers)
    assert response.status_code == status.HTTP_201_CREATED
