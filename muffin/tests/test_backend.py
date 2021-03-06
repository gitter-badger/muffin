# Copyright (C) Electronic Arts Inc.  All rights reserved.

import muffin.backend as backend
import pytest


def test_empty_config(app):
    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        del app.config['SQLALCHEMY_DATABASE_URI']

    backend.init_app(app)

    assert 'SQLALCHEMY_DATABASE_URI' in app.config

    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    assert db_uri.startswith('sqlite')


def test_single_shard(app):
    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        del app.config['SQLALCHEMY_DATABASE_URI']

    d = app.config['DATABASES'] = {}
    ds = d['default'] = {}
    ds['db'] = 'testmuffin'
    backend.init_app(app)

    assert 'SQLALCHEMY_DATABASE_URI' in app.config

    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    assert db_uri.startswith('sqlite')
    assert db_uri.endswith('testmuffin.db')


def test_multiple_shard(app):
    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        del app.config['SQLALCHEMY_DATABASE_URI']

    if 'SQLALCHEMY_BINDS' in app.config:
        del app.config['SQLALCHEMY_BINDS']

    d = app.config['DATABASES'] = {}
    ds = d['default'] = {}
    ds['db'] = 'testmuffin'

    ss = d['second'] = {'type': 'testing'}
    ss['db'] = 'secondshard'

    backend.init_app(app)

    binds = app.config['SQLALCHEMY_BINDS']

    assert 'second' in binds
    ss_uri = binds['second']
    assert ss_uri.startswith('testing')
    assert ss_uri.endswith('secondshard')


def test_set_alchemy_uri(app):
    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        del app.config['SQLALCHEMY_DATABASE_URI']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'ThisWillNotChange'
    backend.init_app(app)
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'ThisWillNotChange'


def test_empty_shard_config(app):
    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        del app.config['SQLALCHEMY_DATABASE_URI']

    app.config['DATABASES'] = {}

    with pytest.raises(backend.BackendException):
        backend.init_app(app)


def test_id_mangling():
    db_id = 322
    shard_id = 12

    entity_id = backend.build_entity_id(db_id, shard_id)
    assert backend.get_db_id(entity_id) == db_id
    assert backend.get_shard_id(entity_id) == shard_id


def test_backend_destroy(test_backend):
    # Just doing a random operation until we actually use the backend fixture
    del test_backend
