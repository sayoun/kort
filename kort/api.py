# -*- coding: utf-8 -*-
import logging

import click
from flask import (
    Flask, request, redirect, g, abort, url_for,
)

from kort.helpers.algo import untokenize_url
from kort.helpers.sqla import init_engine, dispose_engine
from kort.models import Links, DBSession

log = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    if 'url' not in request.form:
        abort(400)
    link = Links.new(request.form['url'])
    location = url_for('forward', token=link.token, _external=True)
    return '', 201, {'Location': location}


@app.route('/<string:token>', methods=['GET'])
def forward(token):
    url = untokenize_url(token)
    if url:
        return redirect(url, code=302)
    abort(404)


@app.cli.command(with_appcontext=False)
@click.argument('resource', metavar='SQLALCHEMY_URL', required=False)
def initdb(resource):
    """Initialize the database.

    usage sample:

    >>> flask initdb sqlite:////tmp/kort.db
    """
    click.echo('Initialize the database')
    init_engine(resource, scoped=True)
    dispose_engine()
    log.info('Setup complete')


def setup_g_vars():
    g.session = DBSession()


def flush_db(response):
    g.session.flush()
    g.session.commit()
    return response


def shutdown_session(exception=None):
    # The session is scoped,
    # this make a new session for every request
    # http://flask.pocoo.org/docs/patterns/sqlalchemy/
    if hasattr(g, 'session'):
        g.session.remove()


def create_app(info=None):
    from kort.conf import configure
    configure()
    return app


app.before_request_funcs = {None: [setup_g_vars]}
app.after_request_funcs = {None: [flush_db]}
app.teardown_appcontext_funcs.extend([shutdown_session])
