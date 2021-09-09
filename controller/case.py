#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: case.py
# Project: FIT
# Created Date: Saturday, July 31st 2021, 5:40:22 pm
# Author: Fabio Zito
# -----
# Last Modified: Tue Sep 07 2021
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


from model.case import CaseModel

from urllib.parse import urlparse

import common.utility as utility

class CaseController:
    
    def __init__(self):
        try:
            self.model = CaseModel()
        except Exception as error:
            raise Exception(error)
    
    def get_cases(self):
        return self.model.get_cases()
    
    def get_names(self):
        return self.model.get_names()
    
    def get_case_from_name(self, name):
        return self.model.get_case_from_name(name)
    
    def get_case_from_id(self, id):
        return self.model.get_case_from_id(id)

    def save(self, case):
        try:
            return self.model.save(case)
        except Exception as error:
            raise Exception(error)
    
    def create_acquisition_directory(self, acquisition_type, config, case_info, content):
        #Directories: Cases -> Case Name -> Acquisition Type -> Acquisiton Content
        if acquisition_type == 'web' :
            content = urlparse(content).netloc
            
        directories = { 'cases_folder': config['cases_folder_' + utility.get_platform()],
                        'case_folder': case_info['name'],
                        'acquisition_type_folder' : acquisition_type,
                        'content_folder' :  content }

        return self.model.create_acquisition_directory(directories)


        