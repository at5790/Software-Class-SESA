import pytest

import data.db_connect as dbc
import states.load as load
import states.query as qry


@pytest.fixture
def loaded_states():
    """Load the states into the test database, and drop them afterwards."""
    load.load_states(db=dbc.TEST_DB)
    yield
    dbc.drop(qry.STATES_COLLECTION, db=dbc.TEST_DB)
