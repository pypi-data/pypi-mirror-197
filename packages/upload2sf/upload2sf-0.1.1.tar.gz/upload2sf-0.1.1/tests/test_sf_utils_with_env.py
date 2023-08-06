from upload2sf.load_environment_variables import set_env_variables_if_missing, verify_env_variables_exist
from upload2sf.sf_utils import sf_connection, run_single_sql_statement, table_exists, get_columns_info
import os
import pytest


@pytest.fixture()
def sf_con():
    set_env_variables_if_missing('upload2sf', 'dev')
    if not verify_env_variables_exist():
        raise Exception("Environment variables not set")
    return sf_connection()

def test_run_single_sql_statement(sf_con):
    q = """SELECT 1 as foo"""
    r = run_single_sql_statement(q, {})
    print(r)
    assert r['FOO'].iloc[0] == 1


def test_table_exists():
    set_env_variables_if_missing('upload2sf', 'dev')
    object_triple = (os.environ.get('DATABASE'), 'INFORMATION_SCHEMA', 'TABLES')
    assert table_exists(object_triple) is True
    object_triple = (os.environ.get('DATABASE'), 'TEST', 'NOT EXISTING')
    assert table_exists(object_triple) is False

def test_get_columns_info():
    set_env_variables_if_missing('upload2sf', 'dev')
    object_triple = (os.environ.get('DATABASE'), 'INFORMATION_SCHEMA', 'TABLES')
    r = get_columns_info(object_triple)
    r = set(r)
    known_columns = {'TABLE_SCHEMA', 'TABLE_NAME', 'TABLE_CATALOG'}
    assert known_columns.issubset(r) is True
