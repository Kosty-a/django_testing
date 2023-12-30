from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTES_HOME = 'notes:home'
USERS_LOGIN = 'users:login'
USERS_LOGOUT = 'users:logout'
USERS_SIGNUP = 'users:signup'
NOTES_LIST = 'notes:list'
NOTES_ADD = 'notes:add'
NOTES_SUCCESS = 'notes:success'
NOTES_DETAIL = 'notes:detail'
NOTES_EDIT = 'notes:edit'
NOTES_DELETE = 'notes:delete'


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )

    def test_pages_availability_for_anonymous_user(self):
        urls = (NOTES_HOME, USERS_LOGIN, USERS_LOGOUT, USERS_SIGNUP)

        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (NOTES_LIST, NOTES_ADD, NOTES_SUCCESS)
        self.client.force_login(self.reader)

        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author_and_reader(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (NOTES_DETAIL, NOTES_EDIT, NOTES_DELETE):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        urls = (
            (NOTES_DETAIL, (self.note.slug,)),
            (NOTES_EDIT, (self.note.slug,)),
            (NOTES_DELETE, (self.note.slug,)),
            (NOTES_ADD, None),
            (NOTES_SUCCESS, None),
            (NOTES_LIST, None),
        )
        login_url = reverse(USERS_LOGIN)

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
