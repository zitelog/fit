#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: case.py
# Project: FIT
# Created Date: Saturday, July 31st 2021, 5:45:25 pm
# Author: Fabio Zito
# -----
# Last Modified: Thu Sep 09 2021
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


from PyQt5 import QtCore, QtGui, QtWidgets

from view.case_form import CaseFormView
from view.error import ErrorView

from controller.case import CaseController

from common.error import ErrorMessage

class CaseView(QtWidgets.QDialog):

    def __init__(self, case_info, parent=None):
        super(CaseView, self).__init__(parent)

        self.setObjectName("CaseView")
        self.resize(479, 311)

        self.setWindowTitle(case_info['name'] + " Case Information (ID:" + str(case_info['id']) + ")")

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setGeometry(QtCore.QRect(10, 270, 441, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.button_box.setCenterButtons(False)
        self.button_box.setObjectName("save")

        self.form = CaseFormView(self)


        self.form.name.setCurrentIndex(self.form.name.findText(case_info['name']))
        self.form.name.setEnabled(False)
        self.form.lawyer_name.setText(case_info['lawyer_name'])
        self.form.proceedings_type.setCurrentIndex(self.form.proceedings_type.findText(case_info['proceedings_type']))
        self.form.courthouse.setText(case_info['courthouse'])
        self.form.proceedings_number.setText(str(case_info['proceedings_number']))


        self.button_box.accepted.connect(lambda: self.accept(case_info))
        self.button_box.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    
    def accept(self, case_info) -> None:

        error_msg = ErrorMessage()

        #load all cases stored in the DB
        try:
           controller = CaseController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                            error_msg.TITLES['form'],
                            error_msg.MESSAGES['get_case_info'],
                            str(error)
                            )

            error_dlg.buttonClicked.connect(self.close)
            error_dlg.exec_()
        
        for key in case_info:
            item = self.form.findChild(QtCore.QObject, key)
            if item is not None:
                if isinstance(item, QtWidgets.QComboBox) is not False and item.currentText():
                     case_info[key] = item.currentText()
                elif isinstance(item, QtWidgets.QLineEdit) is not False and item.text():
                     case_info[key] = item.text()

                     
        #store information case on the local DB
        try:
           controller.save(case_info)
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                            error_msg.TITLES['insert_update_case_info'],
                            error_msg.MESSAGES['insert_update_case_info'],
                            str(error)
                            )

            error_dlg.buttonClicked.connect(self.close)
            error_dlg.exec_()

        return super().accept()
    
    def reject(self) -> None:
        return super().reject()

