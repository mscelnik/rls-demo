""" SQL database services.

By default all services use Azure SQL Server, though you can provide your own SQLAlchemy engine.
"""

from .. import model

DEFAULT_DRIVER = 'ODBC Driver 17 for SQL Server'
DEFAULT_SERVER = '(LocalDB)\\MSSQLLocalDB'
DEFAULT_DATABASE = 'mydb'


def make_mssql_engine(dbname, server, driver=DEFAULT_DRIVER, **kwargs):
    """ Connects an engine to a SQL Server database.
    Anonymous access by default unless credentials provided in kwargs.

    Args:
        dbname (str): Database name.
        server (str): Service URL.
        driver (str, optional): SQL driver name.
        kwargs: Other parameters for the connection string.
    """
    reqd_params = [
        f'DRIVER={{{driver}}}',
        f'SERVER={server}',
        f'DATABASE={dbname}'
    ]
    opt_params = [f'{param.upper()}={{{value}}}' for param,
                    value in kwargs.items()]
    connstr = ';'.join(reqd_params + opt_params)
    return make_mssql_engine_from_connstr(connstr)


def make_mssql_engine_from_connstr(connstr):
    """ Connects an engine to a SQL Server database given a connection string.

    Args:
        connstr (str): Connection string
    """
    import urllib
    import sqlalchemy
    print(connstr)
    safe_connstr = urllib.parse.quote_plus(connstr)
    url = f'mssql+pyodbc:///?odbc_connect={safe_connstr}'
    engine = sqlalchemy.create_engine(url, fast_executemany=True)
    return engine


class SqlService(object):
    """ Generic service to interact with SQL database via ODBC.
    """

    def __init__(self, connector, base=None, **kwargs):
        from sqlalchemy.engine import Engine
        if isinstance(connector, Engine):
            self._engine = connector
        else:
            # Assume it is a connection string.
            self._engine = make_mssql_engine_from_connstr(connector)
        self.base = base
        self.meta = None
        self._session = None
        self._make_session()
        self._load_tables()

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine

    def _make_session(self):
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        return self._session

    def _load_tables(self):
        from sqlalchemy import Table, MetaData
        if self._engine is None:
            return
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)

    def tear_down(self):
        """ CAUTION! Drops all tables from the database.
        """
        # Ensure we have eyes on all tables before dropping them.
        self.meta.reflect(bind=self.engine)
        self.meta.drop_all(self.engine)

    def set_up(self):
        """ CAUTION! Creates all tables in the database.
        """
        if self.base is not None:
            self.base.metadata.create_all(self.engine)
            self._load_tables()
        else:
            raise ValueError('Cannot set up database as declarative base (self.base) is None.')

    def reset_database(self):
        """ CAUTION! Resets the database by dropping all tables and re-creating.
        """
        self.tear_down()
        self.set_up()

    def run_query(self, sql):
        """ Run an SQL query directly on the database, returning the result
        WARNING!: Does not validate SQL prior to execution.
        """
        from sqlalchemy import text
        t = text(sql)
        results = self.session.execute(t)
        self.session.commit()
        return results

    def run_query_file(self, fpath):
        """ Runs an SQL query stored in a text file.

        Args:
            fpath (str): Path to the query file.
        """
        with open(fpath, 'r') as thefile:
            sql = thefile.read()
        return self.run_query(sql)


class MyDbService(SqlService):
    """ Service to interact with a database which confrosm to the MyDB model.
    """

    def __init__(self, connector, **kwargs):
        from ..model.mydb import Base
        super().__init__(connector, base=Base, **kwargs)

    def set_user(self, userid):
        from sqlalchemy import text
        sql = text("EXEC sp_set_session_context @Key=N'UserID', @value=:userid;")
        self.session.execute(sql, params={'userid': userid})
        self.session.commit()

    def query_asset_data(self):
        import pandas as pd
        sql = "SELECT * FROM asset_data"
        df = pd.read_sql(sql, self.engine)
        return df
