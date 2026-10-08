import pytest

import data.manus.fields as flds
import data.manus.query as qry


# new manuscript for each test so referees don't carry over
def new_manu() -> dict:
    return {
        flds.TITLE: 'Test title',
        flds.AUTHOR: 'Test author',
        flds.REFEREES: [],
    }


# should return a list of states
def test_get_states():
    states = qry.get_states()
    assert isinstance(states, list)
    assert qry.TEST_STATE in states


# real state is valid, made up one is not
def test_is_valid_state():
    assert qry.is_valid_state(qry.TEST_STATE)
    assert not qry.is_valid_state('Not a state')


# real action is valid, made up one is not
def test_is_valid_action():
    assert qry.is_valid_action(qry.TEST_ACTION)
    assert not qry.is_valid_action('Not an action')


# assigning a referee moves it to referee review
def test_assign_ref():
    manu = new_manu()
    new_state = qry.handle_action(qry.SUBMITTED, qry.ASSIGN_REF,
                                  manu=manu, ref='Jack')
    assert new_state == qry.IN_REF_REV
    assert 'Jack' in manu[flds.REFEREES]


# removing the last referee goes back to submitted
def test_delete_last_ref():
    manu = new_manu()
    qry.handle_action(qry.SUBMITTED, qry.ASSIGN_REF, manu=manu, ref='Jack')
    new_state = qry.handle_action(qry.IN_REF_REV, qry.DELETE_REF,
                                  manu=manu, ref='Jack')
    assert new_state == qry.SUBMITTED
    assert manu[flds.REFEREES] == []


# withdraw works from every state
def test_withdraw_from_any_state():
    for state in qry.get_states():
        assert qry.handle_action(state, qry.WITHDRAW) == qry.WITHDRAWN


# unknown state should raise an error
def test_bad_state():
    with pytest.raises(ValueError):
        qry.handle_action('Not a state', qry.WITHDRAW)


# can't assign a referee once it's rejected
def test_action_not_allowed():
    with pytest.raises(ValueError):
        qry.handle_action(qry.REJECTED, qry.ASSIGN_REF,
                          manu=new_manu(), ref='Jack')
