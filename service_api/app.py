from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, render_template, make_response, request
from flask_caching import Cache
from werkzeug.exceptions import InternalServerError

from service_api.config import runtime_config
from service_api.constants import CACHE_TIMEOUT
from service_api.logger import logger
from service_api.services.movies_getter import MoviesPeopleGetter

app = Flask(__name__)
app.config.from_object(runtime_config())

cache = Cache(app=app, config={'CACHE_TYPE': 'simple'})


def cache_header(max_age, **ckwargs):
    def decorator(view):
        f = cache.cached(max_age, **ckwargs)(view)

        @wraps(f)
        def wrapper(*args, **wkwargs):
            response = f(*args, **wkwargs)
            response.cache_control.max_age = max_age
            response.cache_control.public = True
            response.expires = response.last_modified + timedelta(seconds=max_age)
            return response.make_conditional(request)
        return wrapper

    return decorator


@app.errorhandler(InternalServerError)
def handle_500(e):
    logger.error(str(e))
    return make_response(
        render_template('error.html')
    )


@app.route('/movies')
@cache_header(CACHE_TIMEOUT)
def get():
    response = make_response(
        render_template(
            'movies.html', movies=MoviesPeopleGetter.get_movies_with_characters()
        )
    )
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    response.headers['mimetype'] = 'text/html'
    response.last_modified = datetime.utcnow()
    response.add_etag()
    return response

