#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: error.py
# Project: FIT
# Created Date: Wednesday, August 18th 2021, 3:15:18 pm
# Author: Fabio Zito
# -----
# Last Modified: Wed Oct 20 2021
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

class ErrorMessage:
    def __init__(self):
        self.TITLES = {
            'acquisition' : 'Acquisition is not possible', 
            'insert_update_case_info' : 'Insert/Update case information is not possible',
            'update_config_info' : 'Update config information is not possible',
            'form' : 'Load data error',
            'software_installation' : 'Software is not installed',
            'capture_packet' : 'Capture error',
            'screen_recoder' : 'Screen Recoder error',
            'mrsign_configuration_options' : 'MRSign configuration options error'
        }

        self.MESSAGES = {
            'get_case_info' : 'An error occurred during get case info from DB! \nSee bellow for more detail.',
            'get_case_id' : 'Case ID not Found \nSee bellow for more detail.',
            'get_configuration' : 'An error occurred during get configuration info from DB! \nSee bellow for more detail.',
            'insert_update_case_info' : 'An error occurred during insert/update case information on the DB! \nSee bellow for more detail.',
            'update_config_info' : 'An error occurred during update config information on the DB! \nSee bellow for more detail.',
            'software_installation' : 'The required software would appear not to be installed on this PC! \nSee bellow for more detail.',
            'capture_packet' : 'An error occurred during network packets acquisition! \nSee bellow for more detail.',
            'screen_recoder' : 'An error occurred during screen recoder acquisition! \nSee bellow for more detail.',
            'mrsign_path' : 'MRSign seem don\'t installed on this path "{}"\nPlease check the configuration.',
            'mrsign_executable' : 'MRSign seem not be an executable file "{}"\nPlease check the installation.',
            'mrsign_hostname_or_port' : 'Hostname or port appear not to be configured\nPlease check the configuration.',
            'mrsign_username_or_password' : 'Username or password appear not to be configured\nPlease check the configuration.'
        }
    