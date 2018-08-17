
import psycopg2

class PsycoPG():
    def __init__(self, database='', user='', pw='', host='', port=''):
        self.conn=psycopg2.connect(database=database, user=user, password=pw, host=host, port=port)

    # def connectPostgreSQL():
    #     conn = psycopg2.connect(database="testdb", user="postgres", password="new.1234", host="127.0.0.1", port="5432")
    #     print 'connect successful!'
    #     cursor = conn.cursor()
    #     cursor.execute('''create table public.member(
    # id integer not null primary key,
    # name varchar(32) not null,
    # password varchar(32) not null,
    # singal varchar(128)
    # )''')
    #     conn.commit()
    #     conn.close()
    #     print 'table public.member is created!'
    #
    # def insertOperate():
    #     conn = psycopg2.connect(database="testdb", user="postgres", password="new.1234", host="127.0.0.1", port="5432")
    #     cursor = conn.cursor()
    #     cursor.execute("insert into public.member(id,name,password,singal)\
    # values(1,'member0','password0','signal0')")
    #     cursor.execute("insert into public.member(id,name,password,singal)\
    # values(2,'member1','password1','signal1')")
    #     cursor.execute("insert into public.member(id,name,password,singal)\
    # values(3,'member2','password2','signal2')")
    #     cursor.execute("insert into public.member(id,name,password,singal)\
    # values(4,'member3','password3','signal3')")
    #     conn.commit()
    #     conn.close()
    #
    #     print 'insert records into public.memmber successfully'

    def select(self, sql):
        # conn = psycopg2.connect(database="testdb", user="postgres", password="new.1234", host="127.0.0.1", port="5432")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def insert(self, sql):
        pass

    def create_database(self, database_name):
        pass

    def create_table(self,sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            return e

    def execute(self,sql):
        cursor=self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()


if __name__ == '__main__':
    # connectPostgreSQL()
    # insertOperate()
    my_psycopg = PsycoPG('test', 'cc5985', 'caichong', 'localhost', '5432')
    my_psycopg.create_table()
    pass
