import pymysql
from zmysql.sql import SQL


class Mysql:
    def __init__(self, *args, **kwargs):
        conn = pymysql.connect(*args, **kwargs, charset='utf8')
        self.cursor = conn.cursor()
        self.db = conn

    def export(self, table):
        return self.get(SQL.all(table))

    def clone(self, table, new):
        """克隆相同schema的新表
        """
        return self.run(self.run(SQL.schema(table))[0][1].replace(table, new))

    def copy(self, table, new):
        """复制表
         db.copy('hangzhou','test1')
        """
        self.clone(table, new)
        self.run(SQL.flush(new, SQL.all(table)))

    def run(self,sql):
        """执行sql语句并输出
        """
        self.cursor.execute(sql)
        self.db.commit();
        rst = self.cursor.fetchall()
        print(rst)
        return rst

    def r(self, sql):
        self.run(sql)

    # @staticmethod
    # def to_table(rst_tuple):
    #     tmp = []
    #     for item in rst_tuple:
    #         tmp.append(list(item))
    #     return table(tmp)

    def exit(self):
        self.cursor.close()
        self.db.close()