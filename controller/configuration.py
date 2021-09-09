#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: configuration.py
# Project: FIT
# Created Date: Tuesday, July 27th 2021, 1:18:14 pm
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

from model.configuration import ConfigurationModel

class ConfigurationController:
    def __init__(self):
        try:
            self.model = ConfigurationModel()
        except Exception as error:
            raise Exception(error)
    
    def get_configuration(self):
        return self.model.get_configuration()
    
    def get_proceedings_type_list(self):
        return self.model.get_proceedings_type_list()
    
    def save(self, config):
        try:
            self.model.save(config)
        except Exception as error:
            raise Exception(error)