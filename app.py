#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: app.py
# Project: FIT
# Created Date: Saturday, June 19th 2021, 8:25:20 am
# Author: Fabio Zito
# -----
# Last Modified: Fri Sep 10 2021
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
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
from view.wizard import WizardView
from view.web import WebView


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wizard = WizardView()
    wizard.init_wizard()
    web = WebView()
    web.hide()
    
    def start_acquisition(acquisition_type, case_id):
        if (acquisition_type == 'web'):
            acquisition_window = web
        elif (acquisition_type == 'mail'):
            pass
        elif (acquisition_type == 'facebook'):
            pass

        acquisition_window.init(case_id)
        acquisition_window.show()

    #Wizard sends a signal when finish button is clicked and case is stored on the DB
    wizard.finished.connect(lambda acquisition_type, case_id: start_acquisition(acquisition_type, case_id))

    wizard.show()

    sys.exit(app.exec_())

    # app = QApplication(sys.argv)
    # app.setApplicationName("Tech35's Web Browser")
    # app.setOrganizationName("Tech35")
    # app.setOrganizationDomain("Google.com")
    

    # window = WebView(8)

    # sys.exit(app.exec_())