import logging.config
import mysql.connector

LOG = logging.getLogger('db.py')


class Database:
    def __init__(self, **kwargs):
        try:
            self._db = mysql.connector.connect(**kwargs)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                LOG.exception(f"Wrong user name {kwargs.setdefault('user')} or password {kwargs.setdefault('password')}")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                LOG.exception(f"Database {kwargs.setdefault('database')} does not exist")
            else:
                LOG.exception(err)
            exit(1)

        self._cursor = self._db.cursor(dictionary=True)

    def __del__(self):
        self._cursor.close()
        self._db.close()

    def fetch_result(self):
        return self._cursor.fetchall()

    def commit(self):
        self._db.commit()

    def execute_query(self, query, *args):
        try:
            self._cursor.execute(query, args)
        except mysql.connector.Error as err:
            LOG.exception("Failed query: {}".format(err))
            exit(1)
