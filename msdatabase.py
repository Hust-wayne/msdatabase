#  -*- coding: utf-8 -*-

import pymssql
import configparser

class MSDataBase(object):

    """
        a operate MS SQLSERVER database class        
        example:

            
            --if you want create database object from file you can do like this
            --db=MSDataBase()
            --file must be db.ini,content like below

            [db]
            host=localhost
            user=sa
            password=
            database=msdb
            charset=utf8

            --query data from database
            from  msdatabase import MSDataBase
            db = MSDataBase(host=host,user=username,password=password,database=database,charset='utf-8')
            result = db.query('select * from users')
            db.close()

            --execute query from database
            from  msdatabase import MSDataBase
            db = MSDataBase(host=host,user=username,password=password,database=database,charset='utf-8')
            result = db.query_no_result("insert into users (username,age) values ('scaluo',45)")
            db.close()
    """
    
    
    def __init__(self, **kargs):
        if not kargs:
            print('load config from file')
            config = configparser.ConfigParser()
            config.read('db.ini')
            print(config.get('db','charset'))
            self.conn = pymssql.connect(host=config.get('db','host'),
                                    user=config.get('db','user'),
                                    password=config.get('db','password'),
                                    database=config.get('db','database'),
                                    charset=config.get('db','charset'))
            
        else:    
            print('load config from input')
            self.conn = pymssql.connect(**kargs)
        self.open = True

    def close(self):
        self.conn.close()
        self.open = False

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def __repr__(self):
        return '<Database open={}'.format(self.open)

    def query(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        retlist = cursor.fetchall()
        return retlist

    def query_cursor(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor

    def query_no_result(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        self.conn.commit()

    def query_batch(self, sqls):
        cursor = self.conn.cursor()
        try:
            for sql in sqls:
                cursor.execute(sql)
            self.conn.commit()
        except pymssql.DatabaseError:
            self.conn.rollback()
            print('batch execute is failure')


if __name__ == '__main__':
    with MSDataBase() as db:
        cursor=db.query_cursor('select * from users')
        for row in cursor:
            print('row=%r'%(row,))
        
   