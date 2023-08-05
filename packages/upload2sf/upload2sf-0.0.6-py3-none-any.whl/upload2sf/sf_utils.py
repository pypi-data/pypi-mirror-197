import os
import pandas as pd
import snowflake
from snowflake.connector.pandas_tools import write_pandas
from snowflake.connector import SnowflakeConnection


def sf_connection() -> SnowflakeConnection:
    """
    : Load environment variables and return a Snowflake connection
    :return: 
    """
    con = snowflake.connector.connect(
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        account=os.environ.get('ACCOUNT'),
        database=os.environ.get('DATABASE'),
        schema=os.environ.get('SCHEMA'),
        role=os.environ.get('ROLE'),
        warehouse=os.environ.get('WAREHOUSE'),
        paramstyle="pyformat"
    )
    return con



def clean_token(s: str, max_length=32) -> str:
    """
    :param s: Text to be cleaned to prevent SQL injection 
    :param max_length: Max length of the string
    :return: string with no special characters
    """
    assert isinstance(s, str)
    bad_chars = [';', ' ', '-', ',', '=', '/', "\\", "'", '"']
    for b in bad_chars:
        s = s.split(b)[0]
    s = s[:max_length]
    return s

def clean_object_triple(object_triple:tuple) -> tuple:
    """
    
    :param object_triple: Objectid triple (database, schema, table)
    :return: object_triple with no special characters
    """
    assert len(object_triple) == 3
    return tuple([clean_token(s) for s in object_triple])

def format_triple_to_identifier(object_triple:tuple) -> str:
    """
    :param object_triple: Objectid triple (database, schema, table)
    :return: Identifier as a string: database.schema.table
    """
    object_triple = clean_object_triple(object_triple)
    return f"""{object_triple[0]}.{object_triple[1]}.{object_triple[2]}"""

def run_single_sql_statement(q: str, params) -> pd.DataFrame:
    """
    Run a single sql statement
    :param q: query
    :param params: parameters
    :return: pandas dataframe
    """
    q = q.strip().split(';')[0]
    with sf_connection() as con:
        r = con.cursor().execute(q, params).fetch_pandas_all()
        con.close()
    return r

def table_exists(object_triple:tuple) -> bool:
    """
    :param object_triple: Objectid triple (database, schema, table)
    :return: boolean indicating if the table exists
    """
    object_triple = clean_object_triple(object_triple)
    database, schema, table = object_triple[0], object_triple[1], object_triple[2]
    information_schema_tables = format_triple_to_identifier((database, 'INFORMATION_SCHEMA', 'TABLES'))
    q = f"""SELECT TABLE_SCHEMA, TABLE_NAME\nFROM IDENTIFIER(%s) as i\nWHERE\ni.TABLE_SCHEMA = (%s) and i.TABLE_NAME = (%s)\n"""
    params = (information_schema_tables, schema, table)
    r = run_single_sql_statement(q, params)
    return r.shape[0] > 0


def get_columns_info(object_triple:tuple) -> list:
    object_triple = clean_object_triple(object_triple)
    database, schema, table = object_triple[0], object_triple[1], object_triple[2]
    information_schema_columns = format_triple_to_identifier((database, 'INFORMATION_SCHEMA', 'COLUMNS'))
    q = f"""SELECT COLUMN_NAME\nFROM IDENTIFIER(%s) as i\nWHERE\ni.TABLE_SCHEMA = (%s) and i.TABLE_NAME = (%s)\nORDER BY i.ORDINAL_POSITION ASC"""
    params = (information_schema_columns, schema, table)
    r = run_single_sql_statement(q, params)
    r = r['COLUMN_NAME'].values
    return r


def compare_columns_info(df: list, db: list) -> bool:
    df = [c.upper() for c in df]
    db = [c.upper() for c in db]
    same_cols = (tuple(df) == tuple(db))
    if same_cols is False:
        raise KeyError(f"""Different columns mapping between df and database: {df} vs {db}""")
    return same_cols

def create_table_if_not_exists(object_triple:tuple, columns: list):
    columns = [clean_token(c).upper() for c in columns]
    objectname = format_triple_to_identifier(object_triple)
    col_list = ",\n".join([f"""{c} VARCHAR""" for c in columns])
    params = (objectname, )
    q = f"""CREATE TABLE IF NOT EXISTS IDENTIFIER(%s) (\n {col_list} , \n PRIMARY KEY (TRANSACTION_ID))"""
    run_single_sql_statement(q, params)
    pass

def truncate_table(object_triple:tuple):
    objectname = format_triple_to_identifier(object_triple)
    q = f"""TRUNCATE TABLE IDENTIFIER(%s)"""
    params = (objectname, )
    run_single_sql_statement(q, params)
    pass


def prepare_table_for_upload(df, object_triple:tuple, overwrite:bool=False):
    df_cols = df.columns.tolist()
    if table_exists(object_triple):
        print('table exists')
        db_cols = get_columns_info(object_triple)
        assert compare_columns_info(df_cols, db_cols)
        print('column matches')
        if overwrite:
            truncate_table(object_triple)
            print('truncate_table')
    else:
        print('create table')
        create_table_if_not_exists(object_triple, df_cols)

def append_with_pandas(df, destination:tuple):
    destination = clean_object_triple(destination)
    with sf_connection() as conn:
        r = write_pandas(df=df, conn=conn, database=destination[0], schema=destination[1], table_name=destination[2], overwrite=False,
                         auto_create_table=False, quote_identifiers=False, create_temp_table=False)
    print('write_pandas: ', r)
    conn.close()

def upload_to_table(df, destination:tuple):
    prepare_table_for_upload(df, destination)
    append_with_pandas(df, destination)
    return None


def get_destination(table:str, database=None, schema=None) -> tuple:
    if database is None:
        database = os.environ.get('DATABASE')
    if schema is None:
        schema = os.environ.get('SCHEMA')
    destination = (database, schema, table)
    return destination