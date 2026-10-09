"""Tests for data/db_connect.py.

These run against the local MongoDB server and a separate test database,
so the app's real data is never touched. Cloud mode is tested by pointing
MONGO_URI at the local server as 127.0.0.1, which tells it apart from
local mode's default of 'localhost'.
"""
import pymongo as pm
import pytest

import data.db_connect as dbc

CLOUD_URI = 'mongodb://127.0.0.1:27017/'
CLOUD_ADDRESS = ('127.0.0.1', 27017)

TEST_DB = 'seDB_test'
TEST_COLLECTION = 'db_connect_tests'
TEST_DOC = {'name': 'Test site', 'capacity': 100}


@pytest.fixture
def no_client(monkeypatch):
    """Reset the shared client, as if connect_db() was never called.

    Closes any connection the test opened.
    """
    monkeypatch.setattr(dbc, 'client', None)
    yield
    if dbc.client is not None:
        dbc.client.close()


def test_connect_cloud_uses_mongo_uri(monkeypatch, no_client):
    """Cloud mode connects to the server named in MONGO_URI."""
    monkeypatch.setenv('CLOUD_MONGO', dbc.CLOUD)
    monkeypatch.setenv(dbc.MONGO_URI, CLOUD_URI)
    assert dbc.connect_db().address == CLOUD_ADDRESS


def test_connect_cloud_without_uri(monkeypatch, no_client):
    """Cloud mode without MONGO_URI raises ValueError and stays unconnected."""
    monkeypatch.setenv('CLOUD_MONGO', dbc.CLOUD)
    monkeypatch.delenv(dbc.MONGO_URI, raising=False)
    with pytest.raises(ValueError):
        dbc.connect_db()
    assert dbc.client is None


@pytest.fixture
def not_connected(monkeypatch, no_client):
    """Seed a test collection with TEST_DOC, leaving db_connect unconnected.

    Seeds through a separate client, so db_connect has no connection until
    the test itself makes one. Drops the collection afterwards.
    """
    monkeypatch.setenv('CLOUD_MONGO', dbc.LOCAL)
    seeder = pm.MongoClient()
    coll = seeder[TEST_DB][TEST_COLLECTION]
    coll.delete_many({})
    coll.insert_one(dict(TEST_DOC))
    yield
    seeder[TEST_DB].drop_collection(TEST_COLLECTION)
    seeder.close()


def test_read_connects(not_connected):
    """read() connects on its own, without connect_db() being called first."""
    assert dbc.read(TEST_COLLECTION, db=TEST_DB) == [TEST_DOC]
