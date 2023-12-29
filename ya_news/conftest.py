from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


@pytest.mark.django_db
@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.mark.django_db
@pytest.fixture
def news_content():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
def comment_content(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def news_id_for_args(news):
    return news.pk,


@pytest.fixture
def comment_id_for_args(comment):
    return comment.pk,


@pytest.fixture
def detail_url_content(news_id_for_args):
    return reverse('news:detail', args=news_id_for_args)


@pytest.fixture
def url_to_comments(detail_url_content):
    return detail_url_content + '#comments'


@pytest.fixture
def edit_url(comment_id_for_args):
    return reverse('news:edit', args=comment_id_for_args)


@pytest.fixture
def delete_url(comment_id_for_args):
    return reverse('news:delete', args=comment_id_for_args)


@pytest.fixture
def form_data():
    return {'text': 'Другой текст комментария'}
