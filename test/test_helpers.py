from helpers import is_taken_shortcode, is_valid_shortcode, generate_unique_shortcode, SHORTCODE_LENGTH
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


def test_is_taken_shortcode_when_shortcode_already_taken(prepare_test_db):
    assert is_taken_shortcode(TEST_SHORTCODE) is True


def test_is_taken_shortcode_when_shortcode_not_taken(prepare_test_db):
    assert is_taken_shortcode('abcdef') is False


def test_generate_unique_shortcode(prepare_test_db):
    generated_shortcode = generate_unique_shortcode()
    assert len(generated_shortcode) is SHORTCODE_LENGTH


def test_is_valid_shortcode_when_shortcode_size_is_not_valid():
    assert is_valid_shortcode('') is False
    assert is_valid_shortcode('abc') is False
    assert is_valid_shortcode('1235') is False
    assert is_valid_shortcode('a1b2_c3d4') is False


def test_is_valid_shortcode_when_shortcode_contains_non_alphanumeric_characters():
    assert is_valid_shortcode('123 45') is False
    assert is_valid_shortcode('abc$de') is False
    assert is_valid_shortcode('!@#$%^') is False
    assert is_valid_shortcode('coola!') is False
    assert is_valid_shortcode('a-bb-a') is False


def test_is_valid_when_shortcode_is_valid():
    assert is_valid_shortcode('coolai') is True
    assert is_valid_shortcode('123456') is True
    assert is_valid_shortcode('c00la1') is True
    assert is_valid_shortcode('a_bb_a') is True
    assert is_valid_shortcode('______') is True
    assert is_valid_shortcode('abc_12') is True
