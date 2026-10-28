import data.db_connect as dbc
import states.load as load
import states.query as qry


def test_get_states_returns_the_loaded_states_by_code(loaded_states):
    expected = {}
    for doc in load.read_states():
        del doc[dbc.MONGO_ID]
        expected[doc['code']] = doc
    assert qry.get_states(db=dbc.TEST_DB) == expected
