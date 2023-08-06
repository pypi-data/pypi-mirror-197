from upload2sf.load_environment_variables import set_env_variables_if_missing, verify_env_variables_exist
from upload2sf.sf_utils import sf_connection
import pytest


@pytest.fixture()
def sf_con():
    set_env_variables_if_missing('upload2sf', 'dev')
    if not verify_env_variables_exist():
        raise Exception("Environment variables not set")
    return sf_connection()

def test_sf_connection(sf_con):
    assert sf_con is not None
    assert sf_con.is_closed() is False
    sf_con.close()

def test_sf_query(sf_con):
    q = """SELECT 1"""
    cur = sf_con.cursor()
    cur.execute(q)
    r = cur.fetchall()
    cur.close()
    sf_con.close()
    assert r[0][0] == 1

