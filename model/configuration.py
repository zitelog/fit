#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: configuration.py
# Project: FIT
# Created Date: Thursday, July 22nd 2021, 6:44:49 pm
# Author: Fabio Zito
# -----
# Last Modified: Mon Aug 30 2021
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
import sys
import os

import common.utility as utility

class ConfigurationModel:
    def __init__(self):

        self.config = self._load_configuration_from_db()
        
    
    def _load_configuration_from_db(self):
        rows = {}
        try:
            conn = sqlite3.connect(os.path.dirname(sys.modules['__main__'].__file__) + '/fit.db') 
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM configuration;")

            for row in cursor.fetchall():
                for index, value in enumerate(row):
                    rows[cursor.description[index][0]] = value

            cursor.close()

        except sqlite3.Error as error:
            raise Exception('Failed read data from sqlite table: (' +  str(error) + ')' )
        finally:
            if conn:
                conn.close()
        
        return rows
        
    def get_configuration(self):
        return self.config
    
    def get_proceedings_type_list(self):
        return self.config['proceedings_type_list'].split(",")
    
    def save(self, config):
        """
        update configuration info
        :param config:
        """
        cases_folder = 'cases_folder_' + utility.get_platform()
        try:
            conn = sqlite3.connect(os.path.dirname(sys.modules['__main__'].__file__) + '/fit.db') 
            sql = ''' UPDATE configuration
                        SET {cases_folder} = ? ,
                        proceedings_type_list = ? ,
                        home_page_url = ?,
                        screen_recorder_options = ?'''.format(cases_folder = cases_folder)
        
            cur = conn.cursor()
            cur.execute(sql, tuple(config.values()))

        except sqlite3.Error as error:
            raise Exception('Failed to update data from sqlite table: (' +  str(error) + ')' )
        finally:
            if conn:
                conn.commit()