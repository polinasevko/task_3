import logging.config
import mysql.connector

LOG = logging.getLogger('db.py')


class Database:
    dbms_connector = {
        'mysql': mysql.connector
    }

    def __init__(self, dbms_name, **kwargs):
        connector = Database._parse_dbms_name(dbms_name)

        try:
            self._db = connector.connect(**kwargs)
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                LOG.exception(f"Wrong user name {kwargs.setdefault('user')} or password {kwargs.setdefault('password')}")
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                LOG.exception(f"Database {kwargs.setdefault('database')} does not exist")
            else:
                LOG.exception(err)
            exit(1)

        self._cursor = self._db.cursor(dictionary=True)

    @staticmethod
    def _parse_dbms_name(dbms_name):
        try:
            connector = Database.dbms_connector[dbms_name.lower()]
            return connector
        except KeyError:
            LOG.exception(f"Wrong DBMS {dbms_name}")
            exit(1)

    def __del__(self):
        self._cursor.close()
        self._db.close()

    def fetch_result(self):
        return self._cursor.fetchall()

    def save(self):
        self._db.commit()

    def execute_query(self, query, *args):
        try:
            self._cursor.execute(query, args)
        except mysql.connector.Error as err:
            self._db.rollback()
            LOG.exception(f"Failed query: {query}\n{err}")
