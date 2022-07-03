"""
Database Operations Class
"""
from configparser import ConfigParser

import pymysql


class DbUtils:

    def connection(self):
        config = ConfigParser()
        config.read('config/config.ini', encoding='utf-8')
        try:
            self.host = config['SQL'].get('HOST')
            self.port = config['SQL'].getint('PORT')
            self.db_name = config['SQL'].get('DB')
            self.user = config['SQL'].get('USER')
            self.password = config['SQL'].get('PASS')
            self.retry_count = config['SQL'].getint('RETRY')
        except Exception as e:
            print(f'Config read failed. {e}')
            raise

        for i in range(self.retry_count):
            try:
                connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    db=self.db_name,
                    user=self.user,
                    password=self.password
                )
            except Exception as e:
                print(f'Database access failed. retry_count{i}. {e}')
                pass
            else:
                return connection
        else:
            raise

    def read(self, query, sql):
        try:
            with self.db_connection.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(query)
                columns = cur.fetchall()
                return columns
        except BaseException as e:
            print(f'Database read failed. SQL:{sql}. {e}')
            raise

    def write(self, query, sql):
        try:
            with self.db_connection.cursor(pymysql.cursors.DictCursor) as cur:
                cur.execute(query)
        except BaseException as e:
            print(f'Database write failed. SQL:{sql}. {e}')
            raise
