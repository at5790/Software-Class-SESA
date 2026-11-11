import pytest

import counties.load as load
import counties.query as qry
import data.db_connect as dbc


@pytest.fixture
def loaded_counties():
    """Load the counties into the test database, and drop them afterwards."""
    load.load_counties(db=dbc.TEST_DB)
    yield
    dbc.drop(qry.COUNTIES_COLLECTION, db=dbc.TEST_DB)
