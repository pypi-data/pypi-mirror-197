from typing import Optional

import pymysql

__all__ = [
    "MysqlOrm",
]


class MysqlOrm(object):
    """数据库的简单使用，结合 SqlFormat 方法使用（临时使用）"""

    def __init__(self, pymsql_connect_config: dict):
        self.connection = pymysql.connect(**pymsql_connect_config)
        self.cursor = self.connection.cursor()

    def insert_data(self, sql_pre: str, sql_after: tuple):
        self.connection.ping(reconnect=True)
        self.cursor.execute(sql_pre, sql_after)
        self.connection.commit()

    def search_data(
        self, sql_pre: str, sql_after: tuple, type: Optional[str] = None
    ) -> (bool, tuple):
        if not type:
            type = "one"

        self.connection.ping(reconnect=True)
        self.cursor.execute(sql_pre, sql_after)
        global select_res
        if type == "all":
            select_res = self.cursor.fetchall()

        elif type == "one":
            select_res = self.cursor.fetchone()

        # 判断查询结果
        return (True, select_res) if select_res else (False, "")

    def update_data(self, sql_pre: str, sql_after: tuple):
        self.connection.ping(reconnect=True)
        self.cursor.execute(sql_pre, sql_after)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
