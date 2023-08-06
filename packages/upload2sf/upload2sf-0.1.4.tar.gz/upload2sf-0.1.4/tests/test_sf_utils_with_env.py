from upload2sf.load_environment_variables import set_env_variables_if_missing, verify_env_variables_exist
from upload2sf.sf_utils import sf_connection, run_single_sql_statement, table_exists, get_columns_info, get_destination, format_triple_to_identifier, upload_df_to_sf
import pandas as pd
import os
import pytest


@pytest.fixture()
def sf_con():
    set_env_variables_if_missing('upload2sf', 'dev')
    if not verify_env_variables_exist():
        raise Exception("Environment variables not set")
    return sf_connection()

@pytest.fixture()
def sample_dataframe() -> pd.DataFrame:
    return pd.DataFrame({'foo': [1, 2, 3], 'bar': ['a', 'b', 'c']})

@pytest.fixture()
def sample_dataframe_with_one_more_column() -> pd.DataFrame:
    return pd.DataFrame({'foo': [1, 2, 3], 'bar': ['a', 'b', 'c'], 'baz': [1, 2, 3]})

@pytest.fixture()
def table_name() -> str:
    return 'test_upload2sf_table'

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

def test_upload_dataframe(sf_con, sample_dataframe, sample_dataframe_with_one_more_column, table_name):
    def return_row_count(table_name):
        q = f"""SELECT COUNT(*) as n_rows FROM IDENTIFIER(%s);"""
        params = (table_name, )
        r = run_single_sql_statement(q, params, df_output=True)
        return r['N_ROWS'].iloc[0]

    destination_triple = get_destination(table_name)
    destination_string = format_triple_to_identifier(destination_triple)

    # Drop table if exists
    q = f"""DROP TABLE IF EXISTS IDENTIFIER(%s);"""
    params = (destination_string, )
    r = run_single_sql_statement(q, params, df_output=False)

    # Case 1: case table does not exist
    print('Case 1: case table does not exist')
    upload_df_to_sf(sample_dataframe, table=table_name)
    assert return_row_count(destination_string) == 3

    # Case 2: case table exists with overwrite=True
    print('Case 2: case table exists with overwrite=True')
    upload_df_to_sf(sample_dataframe, table=table_name, overwrite=True)
    assert return_row_count(destination_string) == 3

    print('Case 3: case table exists with overwrite=False')
    # Case 3: case table exists with overwrite=False
    upload_df_to_sf(sample_dataframe, table=table_name, overwrite=False)
    assert return_row_count(destination_string) == 6

    print('Case 4: case table exists with overwrite=False and one more column')
    # Case 4: case table exists with overwrite=False and one more column
    upload_df_to_sf(sample_dataframe_with_one_more_column, table=table_name, overwrite=True)





