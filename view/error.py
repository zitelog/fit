#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: error.py
# Project: FIT
# Created Date: Wednesday, August 18th 2021, 2:27:31 pm
# Author: Fabio Zito
# -----
# Last Modified: Wed Aug 18 2021
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

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui

class ErrorView(QMessageBox):
    def __init__(self, severity, title, message, details, parent=None):
        super(ErrorView, self).__init__(parent)
        # enable custom window hint
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.setIcon(severity)
        self.setWindowTitle(title)
        self.setText(message)
        self.setInformativeText(details)
        