#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: verifysignature.py
# Project: FIT
# Created Date: Thursday, October 7th 2021, 7:24:28 pm
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



import os
import json

from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets

from view.error import ErrorView
from view.signature import SignatureView
from view.configuration import ConfigurationView

from controller.configuration import ConfigurationController

from common.error import ErrorMessage

import common.utility as utility


class VerySystemModel(QtWidgets.QFileSystemModel):

    def columnCount(self, parent = QtCore.QModelIndex()):
        return super(VerySystemModel, self).columnCount()+1
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return ["Name", "Size", "Type", "Date Modified","Verified"][section]
            if orientation == QtCore.Qt.Vertical:
                return str("List ") + str(section)

    def data(self, index, role):
        if index.column() == self.columnCount() - 1:
            if role == QtCore.Qt.DisplayRole:
                return "YourText"
            if role == QtCore.Qt.TextAlignmentRole:
                return QtCore.Qt.AlignHCenter

        return super(VerySystemModel, self).data(index, role)

class VerifySignatureView(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(VerifySignatureView, self).__init__(*args, **kwargs)

        self.error_msg = ErrorMessage()
        #To start the acquisition it is also necessary load the configuration information from the DB
        try:
            self.config_controller = ConfigurationController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Critical,
                                self.error_msg.TITLES['acquisition'],
                                self.error_msg.MESSAGES['get_configuration'],
                                str(error)
                                )

            error_dlg.buttonClicked.connect(quit)
            error_dlg.exec_()

        self.config = self.config_controller.get_configuration()
        self.folderpath = None
        self.signature = SignatureView(self)
        self.signature.finished.connect(self.__signature_process_is_finished)

        self.setObjectName("VerifySignatureView")
        self.resize(800, 600)
        self.setWindowTitle("Freezing Internet Tool")
        self.setWindowIcon(QtGui.QIcon(os.path.join('asset/images/', 'icon.png')))
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)
    

        #SELECT FOLDER ACQUISITION TO VERIFY
        self.folder_widget = QtWidgets.QWidget(self.central_widget)
        self.folder_widget.setGeometry(QtCore.QRect(30, 50, 701, 31))
        self.folder_widget.setObjectName("folder_widget")
        self.folder_hlayout = QtWidgets.QHBoxLayout(self.folder_widget)
        self.folder_hlayout.setContentsMargins(0, 0, 0, 0)
        self.folder_hlayout.setObjectName("folder_hlayout")
        self.folder_path = QtWidgets.QLineEdit(self.folder_widget)
        self.folder_path.setObjectName("folder_path")
        self.folder_path.textChanged.connect(self.enable_verify_button)
        self.folder_hlayout.addWidget(self.folder_path)
        self.folder_button = QtWidgets.QPushButton(self.folder_widget)
        self.folder_button.setObjectName("folder_button")
        self.folder_hlayout.addWidget(self.folder_button)
        self.folder_button.clicked.connect(self.select_folder)

        #LIST VIEW AREA
        self.model = VerySystemModel()
        self.tree =  QtWidgets.QTreeView(self.central_widget)
        self.tree.setGeometry(QtCore.QRect(30, 100, 701, 341))
        self.tree.setColumnWidth(0, 250)
        self.tree.setAlternatingRowColors(True)
        
        #BOTTOM BUTTONS
        self.buttons_widget = QtWidgets.QWidget(self.central_widget)
        self.buttons_widget.setGeometry(QtCore.QRect(380, 470, 351, 41))
        self.buttons_widget.setObjectName("buttons_widget")
        self.buttons_hlayout = QtWidgets.QHBoxLayout(self.buttons_widget)
        self.buttons_hlayout.setContentsMargins(0, 0, 0, 0)
        self.buttons_hlayout.setObjectName("buttons_hlayout")


        #CONFIGURATION BUTTON
        self.configuration_button = QtWidgets.QPushButton(self.buttons_widget)
        self.configuration_button.setObjectName("configuration_button")
        self.configuration_button.clicked.connect(self.configuration)
        self.buttons_hlayout.addWidget(self.configuration_button)

        #VERIFY BUTTON
        self.verify_button = QtWidgets.QPushButton(self.buttons_widget)
        self.verify_button.setObjectName("verify_button")
        self.verify_button.setEnabled(False)
        self.verify_button.clicked.connect(self.verify_acquisition)
        self.buttons_hlayout.addWidget(self.verify_button)
              
        
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))

        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def init(self, case_id):
        pass

    def reload_configuration(self):
        self.config = self.config_controller.get_configuration()

    def select_folder(self):
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Acquisition Folder', os.path.expanduser(self.config['cases_folder_' + utility.get_platform()]))
        self.folder_path.setText(self.folderpath)
    
    def configuration(self):
        config = ConfigurationView(self)
        config.exec_()

    def verify_acquisition(self):
        self.model.setRootPath(self.folder_path.text())
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.folder_path.text()))

        self.signature.verify(self.folderpath)
    
    def __signature_process_is_finished(self):
        pass

    def enable_verify_button(self):
        file = Path(self.folder_path.text())

        if file.is_dir():
            self.verify_button.setEnabled(True)
        else:
           self.verify_button.setEnabled(False) 

   


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.configuration_button.setText(_translate("VerifySignatureView", "Configuration"))
        self.verify_button.setText(_translate("VerifySignatureView", "Verify"))
        self.folder_button.setText(_translate("VerifySignatureView", "Select Folder"))
    