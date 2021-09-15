#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: wizard.py
# Project: FIT
# Created Date: Wednesday, June 23rd 2021, 12:51:13 pm
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



from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import os

from view.case_form import CaseFormView
from view.error import ErrorView

from controller.case import CaseController

from common.error import ErrorMessage

class CaseInfoPage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(CaseInfoPage, self).__init__(parent)
        self.setObjectName("CaseInfoPage")

        self.case_info = {}

        self.error_msg = ErrorMessage()
        #Get all cases names present on the DB
        try:
           self.case_controller = CaseController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                            self.error_msg.TITLES['form'],
                            self.error_msg.MESSAGES['get_case_info'],
                            str(error)
                            )

            error_dlg.buttonClicked.connect(self.close)
            error_dlg.exec_()

        self.case_names_list = self.case_controller.get_names()

        self.case_form_widget = QtWidgets.QWidget(self)
        self.case_form_widget.setGeometry(QtCore.QRect(0, 0, 795, 515))
        self.case_form_widget.setObjectName("case_form_widget")

        self.form = CaseFormView(self.case_form_widget)
        self.form.setGeometry(QtCore.QRect(0, 0, 400, 200))

        x = (self.case_form_widget.frameGeometry().width()/2) - (self.form.frameGeometry().width()/2) -20
        y = (self.case_form_widget.frameGeometry().height()/2) - (self.form.frameGeometry().height()/2)
        self.form.move(x, y)

        #This allow to edit every row on combox
        self.form.name.setEditable(True)
        self.form.name.setCurrentIndex(-1)
        self.form.name.currentTextChanged.connect(self.completeChanged)
        self.form.case_form_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.form.name)
           
    def isComplete(self):
        if self.form.name.currentText() in self.case_names_list:
            self.set_case_information(self.form.name.currentText())
        else:
            self.clear_case_information()
        return self.form.name.currentText() != ""
    
    def set_case_information(self, name):
        self.case_info = self.case_controller.get_case_from_name(name)
        self.form.lawyer_name.setText(self.case_info['lawyer_name'])
        self.form.proceedings_type.setCurrentIndex(self.form.proceedings_type.findText(self.case_info['proceedings_type']))
        self.form.courthouse.setText(self.case_info['courthouse'])
        self.form.proceedings_number.setText(str(self.case_info['proceedings_number']))
    
    def clear_case_information(self):
        self.form.lawyer_name.setText(None)
        self.form.proceedings_type.setCurrentIndex(-1)
        self.form.courthouse.setText(None)
        self.form.proceedings_number.setText(None)
    


class SelectAcquisitionTypePage(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(SelectAcquisitionTypePage, self).__init__(parent)

        self.setObjectName("SelectAcquisitionType")

        self.acquisition_group_box = QtWidgets.QGroupBox(self)
        self.acquisition_group_box.setEnabled(True)
        self.acquisition_group_box.setGeometry(QtCore.QRect(60, 70, 671, 331))
        self.acquisition_group_box.setObjectName("acquisition_group_box")

        #TEXT AREA RECAP INFO
        self.recap_case_info = QtWidgets.QTextBrowser(self.acquisition_group_box)
        self.recap_case_info.setGeometry(QtCore.QRect(170, 60, 430, 200))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.recap_case_info.setFont(font)
        self.recap_case_info.setReadOnly(True)
        self.recap_case_info.setObjectName("recap_case_info")

        # Create a button group for radio buttons
        self.choise_acquisition_button_group = QtWidgets.QButtonGroup()

        self.choise_acquisition_vertical_widget = QtWidgets.QWidget(self.acquisition_group_box)
        self.choise_acquisition_vertical_widget.setGeometry(QtCore.QRect(20, 60, 121, 161))
        self.choise_acquisition_vertical_widget.setObjectName("choise_acquisition_vertical_widget")
        self.choise_acquisition_vertical_layout = QtWidgets.QVBoxLayout(self.choise_acquisition_vertical_widget)
        self.choise_acquisition_vertical_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.choise_acquisition_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.choise_acquisition_vertical_layout.setSpacing(0)
        self.choise_acquisition_vertical_layout.setObjectName("choise_acquisition_vertical_layout")


        self.web = QtWidgets.QRadioButton(self.choise_acquisition_vertical_widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.web.setFont(font)
        self.web.setChecked(True)
        self.web.setObjectName("web")
        self.choise_acquisition_vertical_layout.addWidget(self.web)
        self.choise_acquisition_button_group.addButton(self.web)




        self.mail = QtWidgets.QRadioButton(self.choise_acquisition_vertical_widget)
        self.mail.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.mail.setFont(font)
        self.mail.setObjectName("mail")
        self.choise_acquisition_vertical_layout.addWidget(self.mail)
        self.choise_acquisition_button_group.addButton(self.mail)

        self.facebook = QtWidgets.QRadioButton(self.choise_acquisition_vertical_widget)
        self.facebook.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.facebook.setFont(font)
        self.facebook.setObjectName("facebook")
        self.choise_acquisition_vertical_layout.addWidget(self.facebook)
        self.choise_acquisition_button_group.addButton(self.facebook)
        



class WizardView(QtWidgets.QWizard):
    finished = QtCore.pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(WizardView, self).__init__(parent)

        self.width = 800
        self.height = 600
        self.setObjectName("WizardView")  



    def init_wizard(self):
        self.setFixedSize(self.width, self.height)
        self.setSizeGripEnabled(False)
        self.setWizardStyle(QtWidgets.QWizard.ModernStyle)
        self.setTitleFormat(QtCore.Qt.RichText)
        self.setSubTitleFormat(QtCore.Qt.RichText)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QtGui.QIcon('asset/images/icon.png'))


        self.case_info_page = CaseInfoPage(self)
        self.select_acquisition_type_page = SelectAcquisitionTypePage(self)

        self.addPage(self.case_info_page)
        self.addPage(self.select_acquisition_type_page)

        self.button(QtWidgets.QWizard.NextButton).clicked.connect(lambda: self.select_acquisition_type_page.recap_case_info.setHtml(self._get_recap_case_info_HTML()))

        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self._create_new_case)


        self.retranslateUi()

    def _create_new_case(self):
        
        buttons = self.select_acquisition_type_page.choise_acquisition_button_group.buttons()
        selected_buttons_index = [buttons[x].isChecked() for x in range(len(buttons))].index(True)
        acquisition_type = buttons[selected_buttons_index].objectName()

        case_id = None
        #store information case on the local DB
        try:
          case_id =  self.case_info_page.case_controller.save(self.case_info_page.case_info)
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                            self.case_info_page.error_msg.TITLES['insert_update_case_info'],
                            self.case_info_page.error_msg.MESSAGES['insert_update_case_info'],
                            str(error)
                            )

            error_dlg.buttonClicked.connect(self.close)
            error_dlg.exec_()

        #Send signal to main loop to start the acquisition window
        self.finished.emit(acquisition_type, case_id)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("FITWizard", "FIT 1.0"))
        self.select_acquisition_type_page.acquisition_group_box.setTitle(_translate("FITWizard", "Tipo Acquizione"))
        self.select_acquisition_type_page.web.setText(_translate("FITWizard", "Web"))
        self.select_acquisition_type_page.mail.setText(_translate("FITWizard", "Mail"))
        self.select_acquisition_type_page.facebook.setText(_translate("FITWizard", "Facebook"))


    def _get_recap_case_info_HTML(self):

        items = self.case_info_page.form.children()
        

        html = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        html += "<html>\n"
        html += "<head>\n"
        html += "<meta name=\"qrichtext\" content=\"1\" />\n"
        html += "<style type=\"text/css\">\n"
        html += "p, li { white-space: pre-wrap; }\n"
        html += "</style>\n"
        html += "</head>\n"
        html += "<body style=\" font-family:\'Arial\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        for i, item in enumerate(items):
            value = ''
            label = ''
            if isinstance(item, QtWidgets.QLabel):
                label = item.text()
                next_item = items[i + 1]
                if isinstance(next_item, QtWidgets.QComboBox) is not False and next_item.currentText():
                    value = next_item.currentText()
                elif isinstance(next_item, QtWidgets.QLineEdit) is not False and next_item.text():
                    value = next_item.text()
                #get info to store on the DB    
                self.case_info_page.case_info[next_item.objectName()] = value
                html += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px;\">\n"
                html += "<span style=\" font-family:\'Arial\',\'Courier New\',\'monospace\'; font-size:14px; font-weight:600; color:#ff0000;\">" + label  + ": </span>\n"
                html += "<span style=\" font-size:14px; font-weight:600;  color:#000000;\">" + value  + "</span>\n"
                html += "</p>\n"
        html += "</body>\n"
        html += "</html>"

        return html
        
        