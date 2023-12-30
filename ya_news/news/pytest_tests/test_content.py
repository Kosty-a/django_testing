import pytest
from django.conf import settings
from django.urls import reverse

HOME_URL = reverse('news:home')


@pytest.mark.django_db
@pytest.mark.usefixtures('news_content')
def test_news_count(client):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('news_content')
def test_news_order(client):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
@pytest.mark.usefixtures('comment_content')
def test_comments_order(client, detail_url_content):
    response = client.get(detail_url_content)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.values('created')
    all_comments_created = [comment['created'] for comment in all_comments]
    assert all_comments_created == sorted(all_comments_created)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, form_on_page',
    (
        (pytest.lazy_fixture('admin_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_page_contains_form(
    detail_url_content, parametrized_client, form_on_page
):
    response = parametrized_client.get(detail_url_content)
    assert ('form' in response.context) is form_on_page
