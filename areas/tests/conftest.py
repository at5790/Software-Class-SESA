import pytest

import areas.load as load
import areas.query as qry
import data.db_connect as dbc


@pytest.fixture
def loaded_areas():
    """Load the areas into the test database, and drop them afterwards."""
    load.load_areas(db=dbc.TEST_DB)
    yield
    dbc.drop(qry.AREAS_COLLECTION, db=dbc.TEST_DB)
