#!/usr/bin/env python3

""" database class, contains everything needed for data storage, retrieval, and management """

import logging
import os
import sqlite3

import pyddle

path = os.path.dirname(pyddle.__file__)
logger = logging.getLogger(__name__)


class database:
    """ database: contains everything needed for data storage, retrieval, and management. 
    when a new instance of this class is created, a table is specified. 
    this will be the table refering to the module that is utilizing the class. 
    optimally, a module should not use a table that is not its own, 
    however i am not omniscient so i dont know if this will change in the future

        [table]: the table used for this instance, will be auto-populated if not already
    """

    def __init__(self, table, debug=False):
        self.table = table
        self.debug = debug
        self.__dbConnect()

    def __dbConnect(self):
        # initialize server connection
        self.dbConn = sqlite3.connect(path + '/database/db.sqlite')
        self.db = self.dbConn.cursor()

        # check if table exists
        c = self.db.execute(""" select name from sqlite_master where type='table' and name='%s'""" % self.table)

        # if table does not exist, create correct table
        if c.fetchone() is None:
            if self.table == 'bootstrap':
                self.db.execute(""" create table bootstrap (ip varchar(50), privKey varchar(1000), pubKey varchar(1000)) """)
            if self.table == 'test':
                self.db.execute(""" create table test (t1 varchar(50), t2 varchar(50)) """)

    def insert(self, data):
        """ insert: orginize given data and insert into table

            [data]: a standard list, this is what will be entered into the columns, in order
        """
        # when inserting n amount of values, we must parse the data into a single string
        values = ''
        n = 0
        for i in data:
            n = n + 1
            if n == len(data):
                values = values + "'" + i + "'"
            else:
                values = values + "'" + i + "', "
        
        # insert into table
        self.db.execute("""insert into %(table)s values (%(values)s)""" % (
            {'table': self.table, 'values': values}))
        self.dbConn.commit()

    def get(self, where, select='*'):
        """ get: query table and retrieve all corresponding entries

            [where]: a sql formatted query filter

            [select]: (optional) specify columns to return
        """

        # execute query
        self.db.execute(""" select %(select)s from %(table)s where %(where)s """ % (
            {'select' : select, 'table': self.table, 'where': where}))

        # get all rows and return
        return self.db.fetchall()
