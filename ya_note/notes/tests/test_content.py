from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

NOTES_LIST = 'notes:list'
NOTES_ADD = 'notes:add'
NOTES_EDIT = 'notes:edit'


class TestContent(TestCase):

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

    def test_notes_list_for_different_users(self):
        users_note_flag = (
            (self.author, True),
            (self.reader, False),
        )
        url = reverse(NOTES_LIST)

        for user, note_flag in users_note_flag:
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertTrue((self.note in object_list) is note_flag)

    def test_pages_contains_form(self):
        urls = (
            (NOTES_ADD, None),
            (NOTES_EDIT, (self.note.slug,))
        )
        self.client.force_login(self.author)

        for name, args in urls:
            url = reverse(name, args=args)
            with self.subTest(name=name):
                response = self.client.get(url)
                self.assertIn('form', response.context)
