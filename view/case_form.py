#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: case_form.py
# Project: FIT
# Created Date: Thursday, August 19th 2021, 10:20:38 am
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

from PyQt5 import QtCore, QtGui, QtWidgets


from view.error import ErrorView

from controller.case import CaseController
from controller.configuration import ConfigurationController

from common.error import ErrorMessage


class CaseFormView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CaseFormView, self).__init__(parent)

        error_msg = ErrorMessage()
        #Get all cases names present on the DB
        try:
           controller = CaseController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                            error_msg.TITLES['form'],
                            error_msg.MESSAGES['get_case_info'],
                            str(error)
                            )

            error_dlg.exec_()

        case_names_list = controller.get_names()

        #Get all cases proceedings type present on the DB
        try:
            config_controller = ConfigurationController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                                error_msg.TITLES['form'],
                                error_msg.MESSAGES['get_configuration'],
                                str(error)
                                )
            error_dlg.exec_()
        
        proceedings_type_list = config_controller.get_proceedings_type_list()

        self.setGeometry(QtCore.QRect(40, 30, 401, 202))
        self.setObjectName("form_layout")

        self.case_form_layout = QtWidgets.QFormLayout(self)
        self.case_form_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.case_form_layout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.case_form_layout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.case_form_layout.setContentsMargins(9, 13, 0, 13)
        self.case_form_layout.setVerticalSpacing(10)
        self.case_form_layout.setObjectName("case_form_layout")

        #CASE_NAME_COMBO
        self.name_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.case_form_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name_label)
        self.name = QtWidgets.QComboBox(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.name.addItems(case_names_list)
        self.case_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name)

        

        #LAWYER_NAME_LINE_EDIT
        self.lawyer_name_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lawyer_name_label.setFont(font)
        self.lawyer_name_label.setObjectName("lawyer_name_label")
        self.case_form_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lawyer_name_label)
        self.lawyer_name = QtWidgets.QLineEdit(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lawyer_name.setFont(font)
        self.lawyer_name.setObjectName("lawyer_name")
        self.case_form_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lawyer_name)


        #PROCEEDINGS_TYPE_COMBO
        self.proceedings_type_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.proceedings_type_label.setFont(font)
        self.proceedings_type_label.setObjectName("proceedings_type_label")
        self.case_form_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.proceedings_type_label)
        self.proceedings_type = QtWidgets.QComboBox(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.proceedings_type.setFont(font)
        self.proceedings_type.setObjectName("proceedings_type")
        self.proceedings_type.addItems(proceedings_type_list)
        self.case_form_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.proceedings_type)


        #COURTHOUSE_LINE_EDIT
        self.courthouse_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.courthouse_label.setFont(font)
        self.courthouse_label.setObjectName("courthouse_label")
        self.case_form_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.courthouse_label)
        self.courthouse = QtWidgets.QLineEdit(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.courthouse.setFont(font)
        self.courthouse.setObjectName("courthouse")
        self.case_form_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.courthouse)


        #PROCEEDINGS_NUMBER_LINE_EDIT
        self.proceedings_number_label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.proceedings_number_label.setFont(font)
        self.proceedings_number_label.setObjectName("proceedings_number_label")
        self.case_form_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.proceedings_number_label)
        self.proceedings_number = QtWidgets.QLineEdit(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.proceedings_number.setFont(font)
        self.proceedings_number.setObjectName("proceedings_number")
        self.case_form_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.proceedings_number)

        self.retranslateUi()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("CaseFormView", "Dialog"))
        self.name_label.setText(_translate("CaseFormView", "Cliente/Caso*"))
        self.lawyer_name_label.setText(_translate("CaseFormView", "Avvocato"))
        self.proceedings_type_label.setText(_translate("CaseFormView", "Tipo procedimento"))
        self.courthouse_label.setText(_translate("CaseFormView", "Tribunale"))
        self.proceedings_number_label.setText(_translate("CaseFormView", "Numero Procedimento"))
