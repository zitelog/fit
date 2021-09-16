#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: case.py
# Project: FIT
# Created Date: Saturday, July 31st 2021, 5:34:42 pm
# Author: Fabio Zito
# -----
# Last Modified: Thu Sep 16 2021
# Modified By: Fabio Zito
# -----
# MIT License
# 
# Copyright (c) 2021 ZF zitelog@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###### 


import sqlite3
from sqlite3 import Error
import sys
import os


class CaseModel:
    def __init__(self):
        self.cases = [] 
        conn = self._create_connection()
        self._load_cases_from_db(conn)

    
    def _create_connection(self, db_file = None):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object
        """

        if db_file == None:
            db_file = 'fit.db'

        return sqlite3.connect(db_file)

    def _load_cases_from_db(self, conn):
        """
        get all cases strored on DB
        :param conn:
        """
        if conn:
            try:
                sql = "SELECT * FROM cases;"
                cur = conn.cursor()
                cur.execute(sql)


                for row in cur.fetchall():
                    new_row = {}
                    for index, value in enumerate(row):
                        new_row[cur.description[index][0]] = value
                    self.cases.append(new_row)

                cur.close()

            except sqlite3.Error as error:
                raise Exception('Failed read data from sqlite table: (' +  str(error) + ')' )
            finally:
                conn.close()

    
    def _update_case_info(self, conn, info):
        """
        update case information
        :param conn:
        :param info:
        """
        
        try:
            sql = ''' UPDATE cases
                    SET name = ? ,
                        lawyer_name = ? ,
                        proceedings_type = ?,
                        courthouse = ?,
                        proceedings_number = ?
                    WHERE id = ?'''
            cur = conn.cursor()
            cur.execute(sql, info)
        except sqlite3.Error as error:
            raise Exception('Failed to update data from sqlite table: (' +  str(error) + ')' )
        finally:
            if conn:
                conn.commit()
    
    def _insert_case_info(self, conn, info):
        """
        insert case information
        :param conn:
        :param info:
        """
        case_id = None

        try:
            sql = 'INSERT INTO cases ({}) VALUES ({})'.format(
                ','.join(info.keys()),
                ','.join(['?']*len(info)))

            cur = conn.cursor()
            cur.execute(sql, tuple(info.values()))

            case_id = cur.lastrowid

            cur.close()

        except sqlite3.Error as error:
            raise Exception('Failed insert data from sqlite table: (' +  str(error) + ')' )
        finally:
            if conn:
                conn.commit()

        return case_id

    def get_cases(self):
        return self.cases
    
    def get_names(self):
        return list(map(lambda x : x['name'], self.cases))

    def get_case_from_name(self, name):
        return next((item for item in self.cases if item["name"] == name), False)
    
    def get_case_from_id(self, id):
        return next((item for item in self.cases if item["id"] == id), False)

    def save(self, case):

        id = None
        conn = self._create_connection()

        if 'id' in case:

            id = case['id']
            case = list(case.values())
            #move id value from the first to last position of list
            case.append(id)
            case.remove(id)

            with conn:
                self._update_case_info(conn, tuple(case))
        else:
            with conn:
                id = self._insert_case_info(conn, case)
        
        conn.close()

        return id
    
    def create_acquisition_directory(self, directories):

        acquisition_type_directory = os.path.join(
                                                os.path.expanduser(directories['cases_folder']), 
                                                directories['case_folder'], 
                                                directories['acquisition_type_folder']
                                            )
        
        acquisition_directory = os.path.join(acquisition_type_directory,  'acquisiton_1')

        if os.path.isdir(acquisition_directory):

            #Get all subdirectories from acquisition directory
            acquisition_directories = [d for d in os.listdir(acquisition_type_directory) if os.path.isdir(os.path.join(acquisition_type_directory, d))]
            
            #select the highest number in sufix name 
            index = max([int(''.join(filter(str.isdigit, item))) for item in acquisition_directories])

            #Increment index and create the new content folder
            acquisition_directory = os.path.join(acquisition_type_directory, 'acquisiton_' + str(index + 1))            

        os.makedirs(acquisition_directory)

        return acquisition_directory
    
    def get_case_directory_list(self, cases_folder):
        
        subfolders = [ f.name for f in os.scandir(cases_folder) if f.is_dir() ]

        return  subfolders