from fastapi import status
from fastapi.testclient import TestClient

from database import get_db
from main import app
from .utils import *
import pytest
from models import ShortUrl

TEST_URL = 'https://www.typetone.ai/'
TEST_SHORTCODE = 'coolai'


@pytest.fixture
def prepare_test_db():
    """Inserts some test data in the database for testing purposes, and clears the database at end of test."""

    # insert a new ShortUrl into database for testing purposes
    short_url = ShortUrl(
        url=TEST_URL,
        shortcode=TEST_SHORTCODE)

    db = TestingSessionLocal()
    db.add(short_url)
    db.commit()
    yield short_url

    # clear the data in the test database to have clean state for every new test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM short_urls;"))
        connection.commit()


client = TestClient(app)

# override get_db to use the test database for testing
app.dependency_overrides[get_db] = override_get_db


def test_get_shortcode_stats_when_shortcode_not_found(prepare_test_db):
    response = client.get('/abcdef/stats')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Shortcode not found'}


def test_get_shortcode_stats_when_shortcode_found(prepare_test_db):
    response = client.get(f'/{TEST_SHORTCODE}/stats')

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get('created') is not None
    assert response.json().get('lastRedirect') is not None
    assert response.json().get('redirectCount') == 0


def test_get_shortcode_when_shortcode_not_found(prepare_test_db):
    response = client.get('/abcdef')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Shortcode not found'}


def test_get_shortcode_redirect_to_url(prepare_test_db):
    response = client.get(f'/{TEST_SHORTCODE}', follow_redirects=False)

    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers['Location'] == TEST_URL


def test_get_shortcode_increase_redirect_count(prepare_test_db):
    response = client.get(f'/{TEST_SHORTCODE}', follow_redirects=False)

    assert response.status_code == status.HTTP_302_FOUND

    db = TestingSessionLocal()
    query_result = db.query(ShortUrl).filter_by(shortcode=TEST_SHORTCODE).first()

    assert query_result.redirects_count == 1


def test_shorten_url_when_url_not_provided(prepare_test_db):
    request_data = {}
    response = client.post('/shorten', json=request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Url not present'}


def test_shorten_url_when_provided_shortcode_already_in_use(prepare_test_db):
    request_data = {'url': 'https://randomurl.com', 'shortcode': TEST_SHORTCODE}
    response = client.post('/shorten', json=request_data)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Shortcode already in use'}


def test_shorten_url_when_provided_shortcode_not_valid(prepare_test_db):
    request_data = {'url': 'https://randomurl.com', 'shortcode': 'invalidshortcode'}
    response = client.post('/shorten', json=request_data)

    assert response.status_code == status.HTTP_412_PRECONDITION_FAILED
    assert response.json() == {'detail': 'The provided shortcode is invalid'}


def test_shorten_url_when_shortcode_not_provided(prepare_test_db):
    request_data = {'url': 'https://randomurl.com'}
    response = client.post('/shorten', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('shortcode') is not None
