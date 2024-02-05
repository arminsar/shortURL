import random
import string

from database import SessionLocal
from models import ShortUrl

SHORTCODE_LENGTH = 6


def is_taken_shortcode(shortcode: str) -> bool:
    """Function to check if the provided shortcode is already present in the database."""
    db = SessionLocal()
    query_result = db.query(ShortUrl).filter_by(shortcode=shortcode).first()
    return query_result is not None


def is_valid_shortcode(shortcode: str) -> bool:
    """Function to check if the provided shortcode is valid.
    Valid shortcodes have a length equal to 6 and consists of only alphanumeric characters and underscores.
    Returns True if the provided shortcode is valid, else returns False."""
    if not len(shortcode) == SHORTCODE_LENGTH:
        return False

    for c in shortcode:
        if not c.isalnum() and not c == '_':
            return False

    return True


def generate_unique_shortcode() -> str:
    """Function to generate a unique shortcode.
    Returns a valid random shortcode which is not already taken in the database."""
    new_shortcode = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=SHORTCODE_LENGTH))

    # try to generate a new shortcode until the generated code is unique
    while True:
        if not is_taken_shortcode(new_shortcode):
            break
        new_shortcode = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=SHORTCODE_LENGTH))

    return new_shortcode
