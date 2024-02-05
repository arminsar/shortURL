from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from starlette import status

import models
from database import engine, get_db
from helpers import is_taken_shortcode, is_valid_shortcode, generate_unique_shortcode
from models import ShortUrl

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class ShortUrlRequest(BaseModel):
    url: str = None
    shortcode: str = None

    model_config = ConfigDict(json_schema_extra={
        'example': {
            'url': 'https://www.typetone.ai/',
            'shortcode': 'coolai'
        }})


@app.get('/{shortcode}/stats', status_code=status.HTTP_200_OK)
async def get_shortcode_stats(shortcode: str, db: Session = Depends(get_db)):
    short_url = db.query(ShortUrl).filter_by(shortcode=shortcode).first()

    if short_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shortcode not found')

    stats = {
        'created': short_url.created,
        'lastRedirect': short_url.last_redirect,
        'redirectCount': short_url.redirects_count
    }

    return stats


@app.get('/{shortcode}', status_code=status.HTTP_200_OK)
async def redirect_shortcode(shortcode: str, db: Session = Depends(get_db)):
    query_result = db.query(ShortUrl).filter_by(shortcode=shortcode).first()

    if query_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Shortcode not found')

    query_result.redirects_count += 1
    db.commit()

    return RedirectResponse(url=query_result.url, status_code=status.HTTP_302_FOUND)


@app.post('/shorten', status_code=status.HTTP_201_CREATED)
async def shorten_url(request: ShortUrlRequest, db: Session = Depends(get_db)):
    if request.url is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Url not present')

    if request.shortcode:
        if not is_valid_shortcode(request.shortcode):
            raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                                detail='The provided shortcode is invalid')
        if is_taken_shortcode(request.shortcode):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Shortcode already in use")
    else:
        request.shortcode = generate_unique_shortcode()

    short_url = ShortUrl(**request.model_dump())

    db.add(short_url)
    db.commit()

    return {
        'shortcode': request.shortcode
    }
