#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the core of sqlite4dummy.

Important class quick link:

- :class:`Column`
- :class:`Table`
- :class:`Index`
- :class:`MetaData`
- :class:`Insert`
- :class:`Select`
- :class:`Update`
- :class:`Delete`


Chinese Doc (中文文档)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

本模块是sqlite4dummy的核心模块, 定义了面向对象的数据库中重要概念的抽象类。

重要的类的API的快速链接:

- :class:`Column`: 列
- :class:`Table`: 表
- :class:`Index`: 索引
- :class:`MetaData`: 元数据
- :class:`Insert`: 增
- :class:`Select`: 查
- :class:`Update`: 改
- :class:`Delete`: 删


class, method, func, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function

try:
    from sqlite4dummy.validate import validator
except ImportError:
    from .validate import validator
    
try:
    from sqlite4dummy.dtype import dtype
except ImportError:
    from .dtype import dtype
    
try:
    from sqlite4dummy.sql import SQL_Param, asc
except ImportError:
    from .sql import SQL_Param, asc

try:
    from sqlite4dummy.pycompatible import _str_type
except:
    from .pycompatible import _str_type

from collections import OrderedDict

###############################################################################
#                               Insert Class                                  #
###############################################################################

class Insert(object):
    """An Insert statement objective oriented constructor.
    
    Insert object are constructed from a table. You can call 
    :meth:`Table.insert()<Table.insert>` to create one for this Table.
    
    Then you can use 
    :meth:`insert_record<sqlite4dummy.engine.Sqlite3Engine.insert_record>`
    and other method to perform record/Row insert, bulk insert, smart insert
    and update (insdate).
    
    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Insert>`
    and read the testcase source code.
    
    **中文文档**
    
    Insert语句的面向对象形式的定义类。
    """
    def __init__(self, table):
        self.table = table
            
    def sql_from_record(self):
        """Generate the 'INSERT INTO table...' sqlite command for recrod
        insertion.
        
        Example::
    
            INSERT INTO table_name VALUES (?,?,...,?);
        
        **中文文档**
        
        生成INSERT INTO table ... Sqlite语句。
        """
        sql_INSERT_INTO = "INSERT INTO\t%s" % self.table.table_name
        sql_KEYWORD_VALUES = "VALUES"
        sql_QUESTION_MARK = "(%s)" % ", ".join(["?"] * len(self.table.all) )
        template = "%s\n%s\n\t%s;"
        self.sql = template % (sql_INSERT_INTO,
                               sql_KEYWORD_VALUES,
                               sql_QUESTION_MARK,)
        
    def sql_from_row(self, row):
        """Generate the 'INSERT INTO table...' sqlite command for row
        insertion.
        
        Example::
        
            INSERT INTO table_name 
                (column1, column2, ..., columnN) 
            VALUES 
                (?,?,...,?);
                
        **中文文档**
        
        生成INSERT INTO table ... Sqlite语句。
        """
        sql_INSERT_INTO = "INSERT INTO\t%s" % self.table.table_name
        sql_COLUMNS = "(%s)" % ", ".join(row.columns)
        sql_KEYWORD_VALUES = "VALUES"
        sql_QUESTION_MARK = "(%s)" % ", ".join(["?"] * len(row.columns) )
        template = "%s\n\t%s\n%s\n\t%s;"
        self.sql = template % (sql_INSERT_INTO,
                               sql_COLUMNS,
                               sql_KEYWORD_VALUES,
                               sql_QUESTION_MARK,)
        
###############################################################################
#                               Select Class                                  #
###############################################################################

class SelectObjectError(Exception):
    pass
        
class Select(object):
    """A Select statement objective oriented constructor.

    To create a Select object, you have to name a list of Column object has to 
    select. And use where(), limit(), offset(), distinct(), order_by() method 
    to specify your selection.

    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Select>`
    and read the testcase source code.

    **中文文档**
    
    Select语句的面向对象形式的定义类。
    :class:`Sqlite3Engine<sqlite4dummy.engine.Sqlite3Engine>` 在执行Select对象
    时会将会调用 :attr:`sql<Select.sql>` 其转化为SQL, 然后执行。
    """
    def __init__(self, args):
        try:
            self.param_list = [c.to_SQL_Param_instance() for c in args]
            
            # 用于储存所有的column_name
            self.all_column_name = [i.column_name for i in self.param_list]
            
            # 用于储存所有的full_name
            self.all_full_name = [i.full_name for i in self.param_list]
    
            # 用于储存SELECT XXX FROM 中 XXX 的部分
            self.all_selected = [i.param for i in self.param_list]
            
            # 用于生成一个临时的Table, 供PickleType Converter编译器使用
            self.temp_table_columns = [
                Column(i.label, i.dtype, skip_validate=True) \
                for i in self.param_list]
        except:
            raise SelectObjectError("Initiation Error")

        self.temp_table = Table("temp_table", MetaData(),
                                *self.temp_table_columns)
        
        # construct SELECT WHAT clause
        self.SELECT_WHAT_clause = "SELECT\t%s" % ",\n\t".\
            join(self.all_selected)
        
        # construct SELECT WHERE clause
        for i in self.param_list:
            try:
                self.SELECT_FROM_clause = "FROM\t%s" % i.table_name
            except:
                pass
        
        self.WHERE_clause = None
        self.ORDER_BY_clause = None
        self.LIMIT_clause = None
        self.OFFSET_clause = None

    def where(self, *args):
        """where() method is used to filter records. It takes arbitrary many 
        comparison of column and value. SQL_Param object is created for 
        each comparison. And finally we produce the WHERE clause SQL.
        
        Example::
        
            >>> from sqlite4dummy
            >>> s = S
            where(column1 >= 3.14, column2.between(1, 100), column3.like("%pattern%"))
            
        Supported operation:
        
            ``>``, ``>=``, ``<``, ``<=``, ``==``, ``!=``
            
        Supported criterion function:
        
            :meth:`~Column.between`, :meth:`~Column.like`, :meth:`~Column.in_`
        
        """
        self.WHERE_clause = "WHERE\t%s" % "\n\tAND ".join([i.param for i in args])
        return self
    
    def order_by(self, *argv):
        """Sort the result-set by one or more columns. you can custom the 
        priority of the orders and choose ascending or descending.
        
        You can define it by three ways.
        
        Method1::
        
            >>> s = Select(table.all).order_by("column_name1", "column_name2")

        Method2::
        
            >>> s = Select(table.all).order_by(asc(table.c.column_name1),
                                               desc(table.c.column_nam2),)
                                               
        Sqlite support :meth:`~Column.asc`, :meth:`~Column.desc`.
        """
        priority = list()
        for i in argv:
            if isinstance(i, Column):
                priority.append(asc(i).param)
            elif isinstance(i, _str_type):
                priority.append("%s ASC" % i)
            else:
                priority.append(i.param)
        self.ORDER_BY_clause = "ORDER BY %s" % ", ".join(priority)
        return self
    
    def limit(self, howmany):
        """LIMIT clause.
        """
        self.LIMIT_clause = "LIMIT %s" % howmany
        return self
    
    def offset(self, howmany):
        """OFFSET clause.
        """
        self.OFFSET_clause = "OFFSET %s" % howmany
        return self
    
    def distinct(self):
        """DISTINCT clause.
        """
        self.SELECT_WHAT_clause = self.SELECT_WHAT_clause.replace(
            "SELECT\t", "SELECT DISTINCT\t")
        self.SELECT_WHAT_clause = self.SELECT_WHAT_clause.replace(
            "\n\t", "\n\t\t")
        return self
    
    def select_from(self, select_obj):
        """SELECT FROM clause.
        """
        self.SELECT_FROM_clause = "FROM\t(%s)" % select_obj.sql.replace(
                                                    "\n", "\n\t")
        return self
    
    @property
    def sql(self):
        """Return SELECT SQL.
        """
        return "\n".join([i for i in [
            self.SELECT_WHAT_clause,
            self.SELECT_FROM_clause,
            self.WHERE_clause,
            self.ORDER_BY_clause,
            self.LIMIT_clause,
            self.OFFSET_clause,
            ] if i ])

###############################################################################
#                               Update Class                                  #
###############################################################################

class UpdateObjectError(Exception):
    pass

class Update(object):
    """A Update statement objective oriented constructor.
    
    An update construct with 
    
    Two major part of UPDATE statement is ``set values`` and ``where``. We provide 
    two methods :meth:`Update.values` and :meth:`Update.where` for this purpose.

    For example::
        
        >>> metadata = MetaData()
        >>> table = Table("test", metadata, 
        ...     Column("_id", dtype.INTEGER),
        ...     Column("_value", dtype.REAL),
        ...     )
        >>> upd = Update(table).values(_value=3.14).where(table.c._id==1)
        >>> upd.sql
        UPDATE    test
        SET    _value = 3.14
        WHERE    test._id = 1

    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Update>`
    and read the testcase source code.

    **中文文档**
    
    Update语句的面向对象形式的定义类。
    """
    def __init__(self, table):
        self.table = table
        self.UPDATE_clause = "UPDATE\t%s" % self.table.table_name
        self.SET_clause = None
        self.WHERE_clause = None
        
    def values(self, **kwarg):
        """Construct set values clause for an UPDATE.
        
        1. absolute update: column_name = value
        2. relative update: column_name1 = column_name2 #operator value
        3. relative update: column_name1 = column_name2 #operator column_name3
        
        Example::
            
            Update(table).values(column1=value1, column2=value2)
            
        **中文文档**
        
        构造UPDATE语句中SET value的SQL语句部分。通常有三类设定更新值的方式:
        
        1. 绝对更新: 列 = 具体值
        2. 相对更新: 列 = 列 #操作符 具体值
        3. 相对更新: 列 = 列 #操作符 列
        """
        res = list()
        for column_name, value in kwarg.items():
            if column_name in self.table.column_names:
                column = self.table.get_column(column_name)
            else:
                raise UpdateObjectError("%s are not column of %s" % (
                    column_name, self.table))
                
            if value == None: # 把值更新为NULL, SQL语句为field = NULL
                res.append("%s = %s" % (column_name, "NULL"))
            else:
                try: # value是SQL_Param对象, 处理相对更新
                    res.append("%s = %s" % (
                        column_name, value.param)) # 直接使用
                except: # value是一个值, 处理绝对更新
                    if isinstance(value, _str_type):
                        res.append("%s = '%s'" % ( # 处理字符串的特殊字符
                            column_name, value.\
                                            replace("'", "''").\
                                            replace('"', '\"')))
                        value = value.replace("'", "''").replace('"', '\"')
                    else:
                        res.append("%s = %s" % ( # 处理sql param
                            column_name, column.to_sql_param(value)))
            
        self.SET_clause = "SET\t%s" % ",\n\t".join(res)
        return self
    
    def where(self, *argv):
        """Define WHERE clause in UPDATE SQL command
        """
        self.WHERE_clause = "WHERE\t%s" % "\n\tAND ".join([i.param for i in argv])
        return self

    @property
    def sql(self):
        """Return UPDATE SQL.
        """
        return "\n".join([i for i in [
            self.UPDATE_clause,
            self.SET_clause,
            self.WHERE_clause,
            ] if i ])

###############################################################################
#                               Delete Class                                  #
###############################################################################

class Delete(object):
    """A Delete statement objective oriented constructor.
    
    The :meth:`Delete.where` method specifies which record or records that should 
    be deleted. If you omit the WHERE clause, all records will be deleted!

    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Delete>`
    and read the testcase source code.
    
    **中文文档**
    
    Delete语句的面向对象形式的定义类。
    """
    def __init__(self, table):
        self.table = table
        self.DELETE_FROM_clause = "DELETE FROM\t%s" % table.table_name
        self.WHERE_clause = None

    def where(self, *argv):
        """where() method is used to filter records. It takes arbitrary many 
        comparison of column and value. SQL_Param object is created for 
        each comparison. And finally we produce the WHERE clause SQL.
        
        Example::
        
            >>> from sqlite4dummy
            >>> s = S
            where(column1 >= 3.14, column2.between(1, 100), column3.like("%pattern%"))
        """
        self.WHERE_clause = "WHERE\t%s" % "\n\tAND ".join([i.param for i in argv])
        return self

    @property
    def sql(self):
        return "\n".join([i for i in [
            self.DELETE_FROM_clause,
            self.WHERE_clause,
            ] if i ])
        
###############################################################################
#                               Column Class                                  #
###############################################################################

class Column(object):
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
                 nullable=True, default=None, primary_key=False, 
                 skip_validate=False):
        if not skip_validate:
            validator.exam_column_name(column_name)
        
        self.column_name = column_name
        self.full_name = column_name
        self.table_name = None
        
        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.primary_key = primary_key
        
        self.to_sql_param = self.data_type.to_sql_param
        self.from_sql_param = self.data_type.from_sql_param
        self.is_pickletype = self.data_type.name == "PICKLETYPE"
        
    def __str__(self):
        """Return column name.
    
        **中文文档**

        返回列名
        """
        return self.full_name
        
    def __repr__(self):
        """Return the string represent the Column object, which can recover 
        the Column object from.
        
        **中文文档**

        返回代表Column的详细信息的字符串。可以通过这个字符串完整地复原出Column
        对象。
        """
        template = "Column('%s', dtype.%s, nullable=%s, default=%s, primary_key=%s)"
        return template % (
                    self.column_name,
                    self.data_type.name,
                    self.nullable,
                    repr(self.default),
                    self.primary_key,
                    )
    
    def bind_table(self, table):
        """Bind a Column to a Table. So we can visit ``Column.table_name`` and 
        ``Column.full_name`` afterwards.
        
        **中文文档**
        
        将Column与Table绑定, 生成两个新的属性: ``Column.table_name``, 和
        ``Column.full_name``。这样在SQL语句中可以选择调用column_name或是full_name。
        
        """
        if isinstance(table, Table):
            self.table_name = table.table_name
            self.full_name = "%s.%s" % (table.table_name, self.column_name)
        else:
            raise TypeError()
    
    # sql expression alias
    def asc(self):
        """Construct an Sql parameter in ORDER BY clause or CREATE INDEX clause.
        """
        return SQL_Param(
            param="%s ASC" % self.full_name,
            column_name=self.column_name,
            full_name=self.full_name,
            table_name=self.table_name,
            sql_name="ASC",
        )
    
    def desc(self):
        """Construct an Sql parameter in ORDER BY clause or CREATE INDEX clause.
        """
        return SQL_Param(
            param="%s DESC" % self.full_name,
            column_name=self.column_name,
            full_name=self.full_name,
            table_name=self.table_name,
            sql_name="DESC",
        )
    
    # comparison operator
    def __lt__(self, other):
        if isinstance(other, Column):
            return SQL_Param("%s < %s" % (
                self.full_name, other.full_name)) 
        else:
            return SQL_Param("%s < %s" % (
                self.full_name, self.to_sql_param(other)) )

    def __le__(self, other):
        if isinstance(other, Column):
            return SQL_Param("%s <= %s" % (
                self.full_name, other.full_name)) 
        else:
            return SQL_Param("%s <= %s" % (
                self.full_name, self.to_sql_param(other)) )
    
    def __eq__(self, other):
        if isinstance(other, Column):
            return SQL_Param("%s = %s" % (
                self.full_name, other.full_name))
        else:
            if other == None: # if Column == None, means column_name is Null
                return SQL_Param("%s IS NULL" % self.full_name)
            else:
                return SQL_Param("%s = %s" % (
                    self.full_name, self.to_sql_param(other)) )
        
    def __ne__(self, other):
        if isinstance(other, Column):
            return SQL_Param("%s != %s" % (
                self.full_name, other.full_name))
        else:
            if other == None: # if Column != None, means column_name NOT Null
                return SQL_Param("%s NOT NULL" % self.full_name)
            else:
                return SQL_Param("%s != %s" % (
                    self.full_name, self.to_sql_param(other)) )
        
    def __gt__(self, other):
        if isinstance(other, Column):
            return SQL_Param("%s > %s" % (
                self.full_name, other.full_name))
        else:
            return SQL_Param("%s > %s" % (
                self.full_name, self.to_sql_param(other)) )
    
    def __ge__(self, other):
        if isinstance(other, Column):
            return SQL_Param("%s >= %s" % (
                self.full_name, other.full_name))
        else:
            return SQL_Param("%s >= %s" % (
                self.full_name, self.to_sql_param(other)) )
    
    def between(self, lowerbound, upperbound):
        """WHERE ... BETWEEN ... AND ... clause.
        """
        if isinstance(lowerbound, Column) and isinstance(upperbound, Column):
            return SQL_Param(
                param="%s BETWEEN %s AND %s" % (
                    self.full_name,
                    lowerbound.full_name, 
                    upperbound.full_name,
                ),
                sql_name="BETWEEN",
            )
        elif isinstance(lowerbound, Column) \
                and (not isinstance(upperbound, Column)):
            return SQL_Param(
                param="%s BETWEEN %s AND %s" % (
                    self.full_name,
                    lowerbound.full_name,
                    self.to_sql_param(upperbound),
                ),
                sql_name="BETWEEN",
            )
        elif isinstance(upperbound, Column) \
                and (not isinstance(lowerbound, Column)):
            return SQL_Param(
                param="%s BETWEEN %s AND %s" % (
                    self.full_name,
                    self.to_sql_param(lowerbound),
                    upperbound.full_name,
                ),
                sql_name="BETWEEN",
            )
        else:
            return SQL_Param(
                param="%s BETWEEN %s AND %s" % (
                    self.full_name,
                    self.to_sql_param(lowerbound),
                    self.to_sql_param(upperbound),
                ),
                sql_name="BETWEEN",
            )

    def like(self, wildcards):
        """WHERE ... LIKE ... clause.
        """
        return SQL_Param(
                param="%s LIKE %s" % (
                    self.full_name, self.to_sql_param(wildcards)),
                sql_name="LIKE",
            )

    def in_(self, choice):
        """WHERE ... IN ... clause.
        """
        return SQL_Param(
                param="%s IN (%s)" % (
                    self.full_name, 
                    ", ".join([self.to_sql_param(i) for i in choice]),
                ),
                sql_name="IN"
            )

    def __add__(self, other):
        """Column + other.
        """
        if isinstance(other, Column):
            return SQL_Param(
                param="%s + %s" % (self.full_name, other.full_name),
                dtype=self.data_type,
            )
        else:
            return SQL_Param(
                param="%s + %s" % (self.full_name, self.to_sql_param(other)),
                dtype=self.data_type,
            )
    
    def __sub__(self, other):
        """Column - other.
        """
        if isinstance(other, Column):
            return SQL_Param(
                param="%s - %s" % (self.full_name, other.full_name),
                dtype=self.data_type,
            )
        else:
            return SQL_Param(
                param="%s - %s" % (self.full_name, self.to_sql_param(other)),
                dtype=self.data_type,
            )
    
    def __mul__(self, other):
        """Column * other.
        """
        if isinstance(other, Column):
            return SQL_Param(
                param="%s * %s" % (self.full_name, other.full_name),
                dtype=self.data_type,
            )
        else:
            return SQL_Param(
                param="%s * %s" % (self.full_name, self.to_sql_param(other)),
                dtype=self.data_type,
            )
    
    def __div__(self, other):
        """Column / other.
        """
        if isinstance(other, Column):
            return SQL_Param(
                param="%s / %s" % (self.full_name, other.full_name),
                dtype=self.data_type,
            )
        else:
            return SQL_Param(
                param="%s / %s" % (self.full_name, self.to_sql_param(other)),
                dtype=self.data_type,
            )
            
    def __truediv__(self, other):
        """Column / other, for python2,3 compatible.
        """
        if isinstance(other, Column):
            return SQL_Param(
                param="%s / %s" % (self.full_name, other.full_name),
                dtype=self.data_type,
            )
        else:
            return SQL_Param(
                param="%s / %s" % (self.full_name, self.to_sql_param(other)),
                dtype=self.data_type,
            )
    
    def __pos__(self):
        """+ Column.
        """
        return SQL_Param(param="+ %s" % self.full_name, dtype=self.data_type)
    
    def __neg__(self):
        """- Column.
        """
        return SQL_Param(param="- %s" % self.full_name, dtype=self.data_type)
    
    def to_SQL_Param_instance(self):
        # 如果只是列的话, param使用column_name, 这样才能让Row能够直接通过列名
        # 而不是全名来访问值。
        return SQL_Param( 
            param="%s" % self.column_name,
            column_name=self.column_name,
            full_name=self.full_name,
            table_name=self.table_name,
            dtype=self.data_type,
        )
        
    def as_(self, label):
        return self.to_SQL_Param_instance().as_(label)
        
###############################################################################
#                                Table Class                                  #
###############################################################################

class DuplicateColumnError(Exception):
    pass

class ColumnCollection(object):
    def __init__(self, *args):
        for column in args:
            if not isinstance(column, Column):
                raise TypeError("ColumnCollection has to be constructed "
                                "by couple of Column objects.")
            else:
                object.__setattr__(self, column.column_name, column)
        if len({column.column_name for column in args}) != len(args):
            raise DuplicateColumnError("Duplicate column name found!")

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
        clause_CREATE_TABLE = "CREATE TABLE %s" % table.table_name
        
        clause_DATATYPE = "\t" + ",\n\t".join(
            [self._column_param(column) for column in table]
            )
            
        if len(table.primary_key_columns) == 0:
            clause_PRIMARY_KEY = ""
        else:
            clause_PRIMARY_KEY = ",\n\tPRIMARY KEY (%s)" % ", ".join(
                                                table.primary_key_columns)

        self.sql = "%s\n(\n%s%s\n)" % (
            clause_CREATE_TABLE, clause_DATATYPE, clause_PRIMARY_KEY)

    def _column_param(self, column):
        """Generate the definition part of 'CREATE TABLE (...)' SQL command
        by column name, data type, constrains.
        
        Example::
        
            movie_id TEXT
            title TEXT DEFAULT 'unknown_title'
            length INTEGER DEFAULT -1
            release_date DATE NOT NULL
        """
        column_name_part = column.column_name
        data_type_part = column.data_type.sqlite_name
        
        if column.nullable == True:
            nullable_part = None
        else:
            nullable_part = "NOT NULL"
            
        if column.default == None:
            default_part = None
        else:
            default_part = "DEFAULT %s" % column.to_sql_param(column.default)
            
        parts = [column_name_part, data_type_part, nullable_part, default_part]
        
        return " ".join([i for i in parts if i])

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
    def __init__(self, table_name, metadata, *args):
        validator.exam_table_name(table_name)
        
        self.table_name = table_name
        self.metadata = metadata
        self.all = list()
        self.column_names = list()
        
        self.primary_key_columns = list()
        self.pickletype_columns = list()
        
        for column in args:
            
            column.bind_table(self) # 将column与Table绑定
            self.all.append(column)
            self.column_names.append(column.column_name)
            
            if column.primary_key: # 定位PRIMARY KEY的列
                self.primary_key_columns.append(column.column_name)
            if column.is_pickletype: # 定位PICKLETYPE的列
                self.pickletype_columns.append(column.column_name)
        
        self.c = ColumnCollection(*self.all)
        self.metadata._add_table(self)
        
        self.create_table_sql = CreateTable(self).sql
        
    def __str__(self):
        """Return table name.
        
        **中文文档**
        
        返回表名。
        """
        return self.table_name
    
    def __repr__(self):
        """Return the string represent the Table object, which can recover 
        the Table object from.
        
        **中文文档**
        
        返回代表Table的详细信息的字符串。可以通过这个字符串完整地复原出Table
        对象。
        """
        template = "Table('%s', MetaData(), \n\t%s,\n)"
        return template % (
            self.table_name, 
            ",\n\t".join([repr(column) for column in self.all])
            )
        
    def __iter__(self):
        """For loop iterate on all instance of Column.
        
        **中文文档**
        
        for ... in table: 返回的是Table中所有Column对象的实例
        """
        return iter(self.all)
    
    def get_column(self, column_name):
        """Get a column by column name.
        
        **中文文档**
        
        根据列名称获取Column对象。
        """
        return getattr(self.c, column_name)
    
    def create(self, engine):
        """Create this table in the database binded to the Sqlite3Engine.
        """
        try:
            create_table_sql = self.create_table_sql
            engine.execute(create_table_sql)
        except Exception as e:
            print(e)
            
    @property
    def drop_table_sql(self):
        """The SQL for deleting this Table.
        """
        return "DROP TABLE %s" % self.table_name
    
    def drop(self, engine):
        """Drop this table in the database binded to the Sqlite3Engine.
        """
        try:
            drop_table_sql = self.drop_table_sql
            engine.execute(drop_table_sql)
            # keep metadata consistant with table
            self.metadata._remove_table(self)
        except Exception as e:
            print(e)
            
    def insert(self):
        """Construct an Insert object.
        """
        return Insert(self)

    def update(self):
        """Construct an Update object.
        """
        return Update(self)

    def delete(self):
        """Construct a Delete object.
        """
        return Delete(self)
    
###############################################################################
#                                 Index  Class                                #
###############################################################################

class IndexObjectError(Exception):
    pass

class Index(object):
    """Represent a index of a :class:`Table`.

    :param index_name: the table name, alpha, digit and understore only.
      Can't start with digit.
    :type index_name: string
    
    :param metadata: Data type object.
    :type metadata: :class:`MetaData`
    
    :param args: index configuration
    :type args: :class:`Column` or :class:`SQL_Param<sqlite4dummy.sql.SQL_Param>`
    
    :param table_name: (default None) create index on which table name.
    :type table_name: string
    
    :param unique: (default False) Whether it's an unique index.
    :type unique: boolean

    For usage example, go :mod:`unittest page<sqlite4dummy.tests.test_Index>`
    and read the testcase source code.

    **中文文档**
    
    Sqlite的CREATE INDEX语句中, 需要指定ON table_name, 而column_name不允许
    table_name.column_name的形式, 只允许原生的column_name。
    
    Index对象可以由, Column对象, 代表column name的字符串, 或是由Column.asc()
    或desc(Column)所生成的_SQL_PARAM对象初始化。其中Column, _SQL_PARAM对象中
    是包含了所属的table对象的信息的。当Index只由字符串生成时, 则要额外指定可
    选参数``table_name``。在其他时候, 我们并不需要显式地指定表名。
    """
    def __init__(self, index_name, metadata, args,
                 table_name=None, unique=False, skip_validate=False):
        if not skip_validate:
            validator.exam_table_name(index_name)
        
        self.index_name = index_name
        self.metadata = metadata
        if table_name:
            self.table_name = str(table_name)
        else:
            self.table_name = None
        self.unique = unique
        self.params = list()

        if self.unique:
            self.CREATE_clause = "CREATE UNIQUE INDEX %s" % self.index_name
        else:
            self.CREATE_clause = "CREATE INDEX %s" % self.index_name
        
        for i in args:
            if isinstance(i, Column): # column
                self.params.append("%s ASC" % i.column_name)
            elif isinstance(i, _str_type): # string
                self.params.append(i.split(".")[-1]) # use column_name only
            else: # _SQL_PARAM
                self.params.append("%s %s" % (i.column_name, i.sql_name))
                
            try: # see if table_name is constant in all argument
                if self.table_name:
                    if self.table_name != i.table_name:
                        raise IndexObjectError("Table name are not unique!")
                else:
                    self.table_name = i.table_name   
            except:
                pass
        
        self.ON_TABLE_clause = "ON %s" % self.table_name
        
        self.COLUMN_clause = "\t" + ",\n\t".join(self.params)
        
        self.metadata._add_index(self)

    def __str__(self):
        """Return index name.
        
        **中文文档**
        
        返回索引名。
        """
        return self.index_name
    
    def __repr__(self):
        """Return the string represent the Index object, which can recover 
        the Index object from.
        
        **中文文档**
        
        返回代表Index的详细信息的字符串。可以通过这个字符串完整地复原出Index
        对象。
        """
        template = ("Index('%s', MetaData(), \n\t%s,\n\t"
                    "table_name=%s,\n\tunique=%s,\n)")
        return template % (
            self.index_name, 
            ",\n\t".join([repr(i) for i in self.params]),
            repr(self.table_name),
            self.unique,
            )

    @property
    def create_index_sql(self):
        """The Sql for creating this Index.
        """
        return "%s\n%s (\n%s\n)" % (self.CREATE_clause, 
                                  self.ON_TABLE_clause, 
                                  self.COLUMN_clause)
    
    def create(self, engine):
        """Create this Index in the database binded to the Sqlite3Engine.
        """
        try:
            create_index_sql = self.create_index_sql
            engine.execute(create_index_sql)
        except Exception as e:
            print("Exception: %s" % e)
            
    @property
    def drop_index_sql(self):
        """The Sql for deleting this Index.
        """
        return "DROP INDEX %s" % self.index_name

    def drop(self, engine):
        """Drop this Index in the database binded to the Sqlite3Engine.
        """
        try:
            drop_index_sql = self.drop_index_sql
            engine.execute(drop_index_sql)
            # keep metadata consistant with table
            self.metadata._remove_index(self)
        except Exception as e:
            print("Exception: %s" % e)
            
###############################################################################
#                               MetaData Class                                #
###############################################################################

class DuplicateTableError(Exception):
    """Raises when duplicated table name been added into metadata.
    """
    pass

class DuplicateIndexError(Exception):
    """Raises when duplicated index name been added into metadata.
    """
    pass

class MetaData(object):
    """A schema information container holds all Table objects in a database and
    their columns' schema definition and constructs.
    
    MetaData are also able to bind to an Sqlite3Engine object. If bound, more
    Table related SQL execution can be easily generated.
    
    Access all table::
    
        MetaData.tables
        
    Access table by table name::
    
        MetaData.get_table(table_name)
        
    Create all table::
    
        MetaData.create_all(engine)
    """
    def __init__(self, bind=None):
        self.t = OrderedDict() # table dict
        self.i = OrderedDict() # index dict
        if bind:
            try:
                self.reflect(bind)
            except Exception as e:
                print(e)
                raise Exception("You cannot bind metadata to '%s'!" % repr(bind))
        else:
            self.bind = bind
    
    def __str__(self):
        """Stringlize metadata detail info.
        """
        if self.bind:
            text_engine = "Binded with %s" % self.bind.dbname
        else:
            text_engine = "Binded with Nothing."
        text_table = "\n".join([repr(table) for table in self.t.values()])
        text_index = "\n".join([repr(index) for index in self.i.values()])
        return "\n".join([text_engine, text_table, text_index])
    
    def _add_table(self, table):
        """Add a Table object to Metadata.
        
        **中文文档**
        
        为MetaData增加一个Table。
        """
        if not isinstance(table, Table):
            raise Exception("Metadata._add_table() method need a Table object "
                            "for input.")
        
        if table.table_name not in self.t:
            self.t[table.table_name] = table
        else:
            raise DuplicateTableError("Duplicate table name found!")
        
    def _remove_table(self, table):
        """Remove a Table by a Table object or it's ``table_name``.
        
        **中文文档**
        
        根据表或表名删除一个表。
        """
        table = self.t.pop(str(table))

    def _add_index(self, index):
        """Add a Index object to Metadata.
        
        **中文文档**
        
        为MetaData增加一个Table。
        """
        if not isinstance(index, Index):
            raise Exception("Metadata._add_index() method need a Index object "
                            "for input.")
            
        if index.index_name not in self.i:
            self.i[index.index_name] = index
        else:
            raise DuplicateIndexError("Duplicate index name found!")
        
    def _remove_index(self, index):
        """Remove an Index by an Index object or it's ``index_name``.
        
        **中文文档**
        
        根据索引或索引名删除一个索引。
        """
        index = self.i.pop(str(index))
        
    def __iter__(self):
        return iter(self.t.values())
    
    def get_table(self, table_name):
        """Access Table by table name.
        """
        return self.t[table_name]
    
    def get_index(self, index_name):
        """Access Index by index name.
        """
        return self.i[index_name]
    
    def create_all(self, engine):
        """Create all table in metadata in database engine. Also bind itself to 
        this engine.
        """
        self.bind = engine
        for table in self.t.values():
            create_table_sql = table.create_table_sql
            try:
                engine.execute(create_table_sql)
                engine.logger.info(create_table_sql)
            except Exception as e:
                engine.logger.info("Exception: %s" % e)

    def drop_all(self, engine):
        """Drop all table in metadata in database engine. Also bind itself to
        this engine.
        """
        self.bind = engine
        for table in self:
            drop_table_sql = table.drop_table_sql
            try:
                engine.execute(drop_table_sql)
                engine.logger.info(drop_table_sql)
                self._remove_table(table.table_name)
            except Exception as e:
                engine.logger.info("Exception: %s" % e)

    def create_all_index(self, engine):
        """Create all index in metadata in database engine. Also bind itself to 
        this engine.
        """
        self.bind = engine
        for index in self.i.values():
            create_index_sql = index.create_index_sql
            try:
                engine.execute(create_index_sql)
                engine.logger.info(create_index_sql)
            except Exception as e:
                engine.logger.info("Exception: %s" % e)

    def drop_all_index(self, engine):
        """Drop all index in metadata in database engine. Also bind itself to
        this engine.
        """
        self.bind = engine
        for index in self.i.values():
            drop_index_sql = index.drop_index_sql
            try:
                engine.execute(drop_index_sql)
                engine.logger.info(drop_index_sql)
                self._remove_index(index.index_name)
            except Exception as e:
                engine.logger.info("Exception: %s" % e)
      
    def reflect(self, engine, pickletype_columns=list()):
        """Read table, column, index metadata from database schema information.
        
        :param engine: Bind to :class:`~sqlite4dummy.engine.Sqlite3Engine`
        
        :param pickletype_columns: pickletype columns' full name list. e.g. 
          [table_name1.column_name1, table_name2.column_name2, ...]
        """
        self.bind = engine

        # find all table name
        table_name_list = [record[0] for record in engine.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table';")]
        
        # extract table structure
        for table_name in table_name_list:
            columns = list()
            for record in engine.execute("PRAGMA table_info(%s)" % table_name):
                (_, column_name, column_type_name, 
                 not_null, default_value, is_primarykey) = record
                # 获得列的全名
                column_fullname = "%s.%s" % (table_name, column_name)
                # 获得列的数据类型的类实例
                column_type = dtype.get_dtype_by_name(column_type_name)
                # 根据特殊规则, 找到pickle type的列
                if (column_fullname in pickletype_columns) and \
                    (column_type.name == "BLOB"):
                    column_type = dtype.PICKLETYPE
                # 获得是否nullable
                nullable = not not_null
                # 获得default value in Python type
                default = column_type.from_sql_param(default_value)
                # 获得是否是primary_key
                primary_key = is_primarykey == 1
                # construct Column
                column = Column(column_name, column_type, skip_validate=True,
                                primary_key=primary_key, nullable=nullable,
                                default=default)
                columns.append(column)
            
            _ = Table(table_name, self, *columns)

        # extract index schema
        for record in engine.execute(
            "SELECT name, tbl_name, sql FROM sqlite_master "
            "WHERE type = 'index' AND sql NOT NULL;"):

            index_name, table_name, sql = record
            params = sql[sql.find("(")+1: sql.find(")")].split(",")
            params = [i.strip() for i in params]

            unique = "CREATE UNIQUE INDEX" in sql
            _ = Index(index_name, self, params,
                      table_name=table_name, 
                      unique=unique, 
                      skip_validate=True)
            