import os
from library import services

connstr = os.getenv('MYDB_CONNECTION_STRING')
mydb = services.sql.MyDbService(connstr)
# mydb.reset_database()
# mydb.run_query_file('src/sql/populate-mydb.sql')
# mydb.run_query_file('src/sql/setup-rls.sql')

df = mydb.query_asset_data()
print(df)

mydb.set_user('de25441a-ea6c-45ea-bbf0-5d102c393e54')
df = mydb.query_asset_data()
print(df)

mydb.set_user('98355e46-0bdb-4d04-9bf2-ddcff230754c')
df = mydb.query_asset_data()
print(df)
