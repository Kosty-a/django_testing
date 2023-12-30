from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

NEWS_HOME = 'news:home'
NEWS_DETAIL = 'news:detail'
USERS_LOGIN = 'users:login'
USERS_LOGOUT = 'users:logout'
USERS_SIGNUP = 'users:signup'
NEWS_EDIT = 'news:edit'
NEWS_DELETE = 'news:delete'


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        (NEWS_HOME, None),
        (NEWS_DETAIL, pytest.lazy_fixture('news_id_for_args')),
        (USERS_LOGIN, None),
        (USERS_LOGOUT, None),
        (USERS_SIGNUP, None)
    ),
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND)
    ),
)
@pytest.mark.parametrize(
    'name',
    (NEWS_EDIT, NEWS_DELETE),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, expected_status, name, comment_id_for_args
):
    url = reverse(name, args=comment_id_for_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (NEWS_EDIT, NEWS_DELETE),
)
def test_redirect_for_anonymous_client(
    name, client, comment_id_for_args
):
    login_url = reverse(USERS_LOGIN)
    url = reverse(name, args=comment_id_for_args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
