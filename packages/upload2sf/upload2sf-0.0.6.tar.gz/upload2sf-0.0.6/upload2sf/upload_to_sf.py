# import pandas as pd
#
# # from stagingfinanzgurutosf.src import latest_excel_as_df_prepared, run_single_sql_statement, formatname, upload_to_table
# # from stagingfinanzgurutosf.src.sf_utils import get_destination
#
#
# def verify_latest_transaction_date(df, stagename:tuple):
#     q = f"""SELECT MAX(TO_DATE(DATE_ENREGISTREMENT)) as TRANSACTION_DATE\nFROM IDENTIFIER(%s)\n"""
#     r = run_single_sql_statement(q, params=(formatname(stagename),))
#     print('latest transaction date in database:', r['TRANSACTION_DATE'][0])
#     print('latest transaction date in df:', df['DATE_ENREGISTREMENT'].max())
#     return None
#
#
# def read_latest_excel() ->pd.DataFrame:
#     df = latest_excel_as_df_prepared().reset_index(drop=False)
#     return df
#
# def upload_to_stg(df:pd.DataFrame, destination:tuple):
#     upload_to_table(df, destination)
#     verify_latest_transaction_date(df, destination)
#
#
# def main():
#     destination = get_destination(table='STG_FINANZGURU')
#     df = read_latest_excel()
#     upload_to_stg(df, destination)
#
#
# if __name__ == '__main__':
#     main()
#
