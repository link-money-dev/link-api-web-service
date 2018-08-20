# -*- coding: UTF-8 -*-

# 基于 sqlite4dummy 的基本架构重新写了一个超简易版本的 sqlite 数据库管理库
# 本程序提供必要的sqlite操作方法，并对一个sqlite数据库进行初始化
# 本程序从自己启动，外部只能调用其方法
# 本程序的主入口程序为 main()

# 请填写下面几个参数：
# 第一个参数为数据库名称
DB_NAME=''


import os
import sqlite3
import sqlite4dummy
import psycopg2

class Column():
    """Represent a Column in a :class:`Table`.

    Construct a Column object::

        >>> from sqlite4dummy import *
        >>> c = Column("employee_id", dtype.TEXT, primary_key=True)
        >>> c
        Column('employee_id', dtype.TEXT, nullable=True, default=None, primary_key=True)

    :param column_name: the column name, alpha, digit and understore only.
      Can't start with digit.
    :type column_name: string

    :param data_type: Data type object.

    :param nullable: (default True) whether it is allow None value.
    :type nullable: boolean

    :param default: (default None) default value.
    :type default: any Python types

    :param primary_key: (default False) whether it is a primary_key.
    :type primary_key: boolean

    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Column>`
    and read the testcase source code.
    """

    def __init__(self, column_name, data_type,
                 nullable=True, default=None, primary_key=False, auto_increment=False):

        self.column_name = column_name
        self.full_name = column_name
        self.table_name = None

        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.primary_key = primary_key
        if primary_key == True:
            self.auto_increment=True
        else:
            self.auto_increment=False


class Table(object):
    """Represent a table in a database.

    Define a Table::

        >>> from sqlite4dummy import *
        >>> metadata = MetaData()
        >>> mytable = Table("mytable", metadata,
                Column("mytable_id", dtype.INTEGER, primary_key=True),
                Column("value", dtype.TEXT),
                )

    columns can be accessed by table.c.column_name::

        >>> mytable.c.mytable_id # return a Column object
        _id

    :param table_name: the table name, alpha, digit and understore only.
      Can't start with digit.
    :type table_name: string

    :param metadata: Data type object.
    :type metadata: :class:`MetaData`

    :param args: list of Column object
    :type args: :class:`Column`

    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Table>`
    and read the testcase source code.

    **中文文档**

    :class:`sqlite4dummy.schema.Table` 是抽象数据表对象类。

    定义Table的方法如下::

        >>> from sqlite4dummy import *
        >>> metadata = MetaData() # 定义metadata
        >>> mytable = Table("mytable", metadata, # 定义表名, metadata和列
                Column("mytable_id", dtype.INTEGER, primary_key=True),
                Column("value", dtype.TEXT),
                )

    从Table中获得Column对象有如下两种方法::

        >>> mytable.c._id
        _id

        >>> mytable.get_column("_id")
        _id
    """

    def __init__(self, table_name, columns, auto_ID=True):

        self.table_name = table_name
        self.all = list()
        self.column_names = list()

        self.primary_key_columns = list()
        self.pickletype_columns = list()

        self.columns=[]

        if auto_ID==True:
            ID_column=Column(column_name="ID",data_type="INTEGER",nullable=False,default=0,primary_key=True)
            self.columns.append(ID_column)
        self.columns.extend(columns)

        for column in columns:
            self.column_names.append(column.column_name)
            if column.primary_key:  # 定位PRIMARY KEY的列
                self.primary_key_columns.append(column.column_name)

        self.create_table_sql = CreateTable(self).sql



class CreateTable(object):
    """Generate 'CREATE TABLE' SQL statement.

    Example::

        CREATE TABLE table_name
        (
            column_name1 dtype1 CONSTRAINS,
            column_name2 dtype2 CONSTRAINS,
            PRIMARY KEY (column, ...),
            FOREIGN KEY (table_column, ...)
        )

    **中文文档**

    创建Table的抽象类, 用于根据Schema生成CREATE TABLE ...的SQL语句。目前不支持
    FOREIGN KEY语法。
    """

    def __init__(self, table):
        clause_CREATE_TABLE = "CREATE TABLE {} ".format(table.table_name)
        field_list = []
        for column in table.columns:
            field_list.append(column.column_name+"\t"+column.data_type+"\t"+
                              ("NOT NULL" if column.nullable==False else "") +"\t" +
                              ("PRIMARY KEY\tAUTOINCREMENT" if column.primary_key==True else ""))
        clause_DATATYPE=",".join(field_list)
        self.sql="%s\n(\n%s\n)" % (
            clause_CREATE_TABLE, clause_DATATYPE)

        # query_string += ",".join(field_list)
        # query_string += ");"
        # clause_CREATE_TABLE = "CREATE TABLE %s" % table.table_name
        #
        # clause_DATATYPE = "\t" + ",\n\t".join(
        #     [self._column_param(column) for column in table]
        # )
        #
        # if len(table.primary_key_columns) == 0:
        #     clause_PRIMARY_KEY = ""
        # else:
        #     clause_PRIMARY_KEY = ",\n\tPRIMARY KEY (%s)" % ", ".join(
        #         table.primary_key_columns)
        #
        # self.sql = "%s\n(\n%s%s\n)" % (
        #     clause_CREATE_TABLE, clause_DATATYPE, clause_PRIMARY_KEY)


class SQLManager():
    def __init__(self, db_name):
        self.db_name=db_name
        # 创建一个空文件，如果存在，则跳过
        if os.path.exists(db_name):
            print("File already exists! Try to connect to this file!")
        else:
            f=open(db_name,'w')
            f.close()
        # 连接到该文件
        self.conn=sqlite3.connect(db_name)

    def reconnet(self):
        self.conn.close()
        self.conn=sqlite3.connect(self.db_name)

    def close(self):
        self.conn.close()

    def insert_into_table(self, table_name, data):
        # 判断table是否存在？
        # SELECT count(*) FROM sqlite_master WHERE type='table' AND name='要查询的表名';
        c=self.conn.cursor()
        cursor = c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='%s'" % table_name)
        a=1
        pass

    def select(self):
        pass

    def execute(self, sql):
        try:
            c = self.conn.cursor()
            result=c.execute(sql)
            self.conn.commit()
            return result.fetchall()
        except Exception as e:
            print(e)

    def execute_many(self,sql,args):
        self.conn.executemany(sql,args)
        self.conn.commit()

class PGManager():
    def __init__(self, database='', user='', pw='', host='', port=''):
        self.conn_args={'database':database, 'user':user, 'password':pw, 'host':host, 'port':port}

    def execute(self,sql):
        self.conn = psycopg2.connect(**self.conn_args)
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()
        self.conn.close()

    def select(self, sql):
        self.conn = psycopg2.connect(**self.conn_args)
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        self.conn.close()
        return rows

    def execute_many(self,query, sql_sequence):
        self.conn = psycopg2.connect(**self.conn_args)
        cursor=self.conn.cursor()
        cursor.executemany(query, sql_sequence)
        self.conn.commit()
        self.conn.close()

    def close(self):
        self.conn.close()