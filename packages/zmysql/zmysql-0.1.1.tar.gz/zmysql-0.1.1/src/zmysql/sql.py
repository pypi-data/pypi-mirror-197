def add_cond(q, cond):
    """ sql条件拼接"""
    if 'where' in q:
        q += ' and ' + cond
    else:
        q += ' where ' + cond
    return q


class SQL:
    def new_db(database):
        return 'create database %s' % database

    def change_db(database):
        return 'use %s' % database

    @staticmethod
    def tables():
        """列出库下所有表
        db.run(s.tables())"""
        return "show tables"

    def new(table, **params):
        """创建表
        db.run(s.new('people',name='varchar(30)',age='int'))
        """
        param_str = ','.join(['%s %s' % (key, value) for key, value in params.items()])
        return "create table %s(%s)" % (table, param_str)

    def rm(table):
        """删除表
        db.r(s.rm('people'))
        """
        return 'drop table %s' % table

    def all(table, items='*'):
        """
        db.run(s.all('zhipin'))
        db.run(s.all('zhipin','title'))"""
        return 'select %s from %s' % (items, table)

    def some(table, pick, cond=''):
        """获取部分记录
        db.run(s.some('zhipin', 'salary>10000'))
        """
        if cond:
            return """select %s from %s where %s""" % (pick, table, cond)
        else:
            return """select %s from %s""" % (pick, table)

    def flush(table, query):
        """批量写入
        sql = s.all('zhipin','substring_index(substring_index(salary,"-",-1),"K",1)')
        db.run(s.flush('table(salary_high)','%s'%sql))
        """
        return "insert into %s %s" % (table, query)

    def rank(rank, query):
        return "%s sort by %s" % (query, rank)

    def count(table):
        if (table.find('select') >= 0):
            return 'select count(*) from (%s) as tmp' % (table)
        else:
            return 'select count(*) from %s' % (table)

    def add(table, data):
        """增加记录
        db.run(sql.add('student',{'name':'rose','age':19}))
        """
        params = data.keys()
        values = data.values()
        values = ['"%s"' % item if isinstance(item, str) else str(item) for item in values]
        return "insert into %s(" % table + ','.join(params) + ") value (" + \
               ','.join(values) + ')'

    def rename(table, name):
        """重命名表
        db.run(s.rename('zhipin','zhipin_gx'))
        """
        return 'alter table %s rename %s' % (table, name)

    def add_col(table, column, dtype):
        """增加列
        db.run(s.del_row('zhipin','salary_high','int'))
        """
        return 'alter table %s add %s %s' % (table, column, dtype)

    def schema(table):
        """表模式
        db.run(sql.schema('student'))
        """
        return 'show create table %s' % table

    def empty(table):
        """清空表
        db.run(s.empty('military'))
        """
        return 'delete from %s' % table

    def del_row(table, cond):
        """删除行
        db.run(s.del_row('zhipin','job_id is null'))
        """
        return 'delete from %s where %s' % (table, cond)

    def del_col(table, column):
        """删除列
        db.run(s.del_col('zhipin','salary_high'))"""
        return 'alter table %s drop %s' % (table, column)