#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: configuration.py
# Project: FIT
# Created Date: Friday, August 20th 2021, 12:45:26 am
# Author: Fabio Zito
# -----
# Last Modified: Thu Sep 16 2021
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

from PyQt5 import QtCore, QtGui, QtWidgets

from view.error import ErrorView

from controller.configuration import ConfigurationController

from common.error import ErrorMessage
import common.utility as utility

class ConfigurationView(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ConfigurationView, self).__init__(parent)

        self.error_msg = ErrorMessage()
        
        try:
            self.controller = ConfigurationController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                                self.error_msg.TITLES['form'],
                                self.error_msg.MESSAGES['get_configuration'],
                                str(error)
                                )

            error_dlg.buttonClicked.connect(self.close)
            error_dlg.exec_()

        self.config = self.controller.get_configuration()

        #Screen Recorder option stored on DB
        self.current_sro = json.loads(self.config['screen_recorder_options'])

        self.setObjectName("ConfigurationView")
        self.resize(722, 480)

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        
        self.tabs = QtWidgets.QTabWidget(self)
        self.tabs.setGeometry(QtCore.QRect(0, 0, 721, 431))
        self.tabs.setObjectName("tabs")

        ################ TAB GENERAL ###################
        self.general = QtWidgets.QWidget()
        self.general.setObjectName("general")
        
        #CASES FOLDER
        self.group_box_cases_folder = QtWidgets.QGroupBox(self.general)
        self.group_box_cases_folder.setGeometry(QtCore.QRect(10, 30, 691, 91))
        self.group_box_cases_folder.setObjectName("group_box_cases_folder")
        self.cases_folder = QtWidgets.QLineEdit(self.group_box_cases_folder)
        self.cases_folder.setGeometry(QtCore.QRect(20, 40, 601, 22))
        self.cases_folder.setObjectName("cases_folder")
        self.tool_button_cases_folder = QtWidgets.QToolButton(self.group_box_cases_folder)
        self.tool_button_cases_folder.setGeometry(QtCore.QRect(640, 40, 27, 22))
        self.tool_button_cases_folder.setObjectName("tool_button_cases_folder")
        self.tool_button_cases_folder.clicked.connect(self._select_cases_folder)



        #HOME PAGE
        self.group_box_home_page_url = QtWidgets.QGroupBox(self.general)
        self.group_box_home_page_url.setGeometry(QtCore.QRect(10, 140, 691, 91))
        self.group_box_home_page_url.setObjectName("group_box_home_page_url")
        self.home_page_url = QtWidgets.QLineEdit(self.group_box_home_page_url)
        self.home_page_url.setGeometry(QtCore.QRect(20, 40, 601, 22))
        self.home_page_url.setObjectName("home_page_url")
        


        #PROCEEDINGS TYPE LIST
        self.group_box_proceedings_type_list = QtWidgets.QGroupBox(self.general)
        self.group_box_proceedings_type_list.setGeometry(QtCore.QRect(10, 250, 691, 131))
        self.group_box_proceedings_type_list.setObjectName("group_box_proceedings_type_list")
        self.proceedings_type_list = QtWidgets.QPlainTextEdit(self.group_box_proceedings_type_list)
        self.proceedings_type_list.setGeometry(QtCore.QRect(20, 30, 601, 87))
        self.proceedings_type_list.setObjectName("proceedings_type_list")
        
        
        #Add tab general on tabs bar
        self.tabs.addTab(self.general, "")


        ################ TAB SCREEN RECORDER OPTIONS ###################
        
        self.screen_recorder_options = QtWidgets.QWidget()
        self.screen_recorder_options.setObjectName("Screen Recorder Options")

        self.enabled_checkbox = QtWidgets.QCheckBox("Enable Screen Recorder", self.screen_recorder_options)
        self.enabled_checkbox.setGeometry(QtCore.QRect(10, 30, 270, 70))
        self.enabled_checkbox.stateChanged.connect(self._is_enabled_screen_recorder)
        self.enabled_checkbox.setObjectName("enabled")

        #RESOLUTION
        self.group_box_resolution = QtWidgets.QGroupBox(self.screen_recorder_options)
        self.group_box_resolution.setGeometry(QtCore.QRect(10, 90, 270, 70))
        self.group_box_resolution.setObjectName("group_box_resolution")
        self.form_layout_resolution = QtWidgets.QWidget(self.group_box_resolution)
        self.form_layout_resolution.setGeometry(QtCore.QRect(20, 30, 222, 24))
        self.form_layout_resolution.setObjectName("form_layout_resolution")
        self.horizontal_layout_resolution = QtWidgets.QHBoxLayout(self.form_layout_resolution)
        self.horizontal_layout_resolution.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_resolution.setObjectName("horizontal_layout_resolution")


        #WIDTH
        self.width_label_resolution = QtWidgets.QLabel(self.form_layout_resolution)
        self.width_label_resolution.setObjectName("width_label_resolution")
        self.horizontal_layout_resolution.addWidget(self.width_label_resolution)
        self.width_resolution = QtWidgets.QLineEdit(self.form_layout_resolution)
        self.width_resolution.setObjectName("width_resolution")
        self.horizontal_layout_resolution.addWidget(self.width_resolution)
        #HEIGHT
        self.height_label_resolution = QtWidgets.QLabel(self.form_layout_resolution)
        self.height_label_resolution.setObjectName("height_label_resolution")
        self.horizontal_layout_resolution.addWidget(self.height_label_resolution)
        self.height_resolution = QtWidgets.QLineEdit(self.form_layout_resolution)
        self.height_resolution.setObjectName("height_resolution")
        self.horizontal_layout_resolution.addWidget(self.height_resolution)
        
        
        #FPS
        self.group_box_fps = QtWidgets.QGroupBox(self.screen_recorder_options)
        self.group_box_fps.setGeometry(QtCore.QRect(310, 90, 160, 70))
        self.group_box_fps.setObjectName("group_box_fps")
        self.fps = QtWidgets.QSpinBox(self.group_box_fps)
        self.fps.setGeometry(QtCore.QRect(20, 30, 80, 22))
        self.fps.setObjectName("fps")
        
        
        #CODEC
        self.group_box_codec = QtWidgets.QGroupBox(self.screen_recorder_options)
        self.group_box_codec.setGeometry(QtCore.QRect(510, 90, 160, 70))
        self.group_box_codec.setObjectName("group_box_codec")
        self.codec = QtWidgets.QComboBox(self.group_box_codec)
        self.codec.setGeometry(QtCore.QRect(20, 30, 80, 22))
        self.codec.setObjectName("codec")
        self.codec.setDisabled(True)

        #FILE NAME
        self.group_box_filename = QtWidgets.QGroupBox(self.screen_recorder_options)
        self.group_box_filename.setGeometry(QtCore.QRect(10, 190, 661, 91))
        self.group_box_filename.setObjectName("group_box_filename")
        self.filename = QtWidgets.QLineEdit(self.group_box_filename)
        self.filename.setGeometry(QtCore.QRect(20, 40, 601, 22))
        self.filename.setObjectName("filename")
        
        
        #Add tab screen_recorder_options on tabs bar
        self.tabs.addTab(self.screen_recorder_options, "")

         ################ END TABS ###################

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(520, 440, 192, 28))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self._set_current_config_values()

        self.retranslateUi(self)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def _set_current_config_values(self):
        self.cases_folder.setText(self.config['cases_folder_' + utility.get_platform()])
        self.home_page_url.setText(self.config['home_page_url'])
        self.proceedings_type_list.setPlainText(self.config['proceedings_type_list'])
        self.enabled_checkbox.setChecked(bool(self.current_sro['enabled']))
        width, height = tuple(self.current_sro['resolution'])
        self.width_resolution.setText(str(width))
        self.height_resolution.setText(str(height))
        self.fps.setValue(self.current_sro['fps'])
        self.codec.addItem(self.current_sro['codec'])
        self.filename.setText(self.current_sro['filename'])

        self._is_enabled_screen_recorder()

    def _is_enabled_screen_recorder(self):
        self.group_box_resolution.setEnabled(self.enabled_checkbox.isChecked())
        self.group_box_fps.setEnabled(self.enabled_checkbox.isChecked())
        self.group_box_codec.setEnabled(self.enabled_checkbox.isChecked())
        self.group_box_filename.setEnabled(self.enabled_checkbox.isChecked())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Fit Configuration"))
        self.group_box_cases_folder.setTitle(_translate("Form", "Cases Folder"))
        self.tool_button_cases_folder.setText(_translate("Form", "..."))
        self.group_box_home_page_url.setTitle(_translate("Form", "Home Page URL"))
        self.group_box_proceedings_type_list.setTitle(_translate("Form", "Proceedings Type List (comma character is separator)"))
        self.tabs.setTabText(self.tabs.indexOf(self.general), _translate("Form", "General"))
        self.group_box_resolution.setTitle(_translate("Form", "Resolution"))
        self.width_label_resolution.setText(_translate("Form", "width:"))
        self.height_label_resolution.setText(_translate("Form", "height:"))
        self.group_box_fps.setTitle(_translate("Form", "Frame per Second (fps)"))
        self.group_box_codec.setTitle(_translate("Form", "Codec"))
        self.group_box_filename.setTitle(_translate("Form", "File Name"))
        self.tabs.setTabText(self.tabs.indexOf(self.screen_recorder_options), _translate("Form", "Screen Recorder Options"))

    def _select_cases_folder(self):
        cases_folder = QtWidgets.QFileDialog.getExistingDirectory(self,
                       'Select Cases Folder', 
                       os.path.expanduser(self.cases_folder.text()),
                       QtWidgets.QFileDialog.ShowDirsOnly)
        self.cases_folder.setText(cases_folder)
    
    def _get_current_config_values(self):
        #General config information
        for key in self.config:
            search_keyword = key
            #In the GUI the cases folder it doesn't depend on to OS, so we need normalize the key value
            if 'cases_folder' in key:
                search_keyword = 'cases_folder'

            item = self.findChild(QtCore.QObject, search_keyword)
            if item is not None:
                if isinstance(item, QtWidgets.QComboBox) is not False and item.currentText():
                     self.config[key] = item.currentText()
                elif isinstance(item, QtWidgets.QLineEdit) is not False and item.text():
                     self.config[key] = item.text()
                elif isinstance(item, QtWidgets.QPlainTextEdit) is not False and item.toPlainText():
                     self.config[key] = item.toPlainText()
        
        #Screen Recorder Options
        for key in self.current_sro:
            if 'resolution' in key:
               width = self.findChild(QtCore.QObject, 'width_resolution')
               if width is not None:
                   width = width.text()
               height = self.findChild(QtCore.QObject, 'height_resolution')
               if height is not None:
                   height = height.text()

               self.current_sro['resolution'] = [width, height]
            else:
                item = self.findChild(QtCore.QObject, key)
                if item is not None:
                    if isinstance(item, QtWidgets.QComboBox) is not False and item.currentText():
                        self.current_sro[key] = item.currentText()
                    elif isinstance(item, QtWidgets.QLineEdit) is not False and item.text():
                        self.current_sro[key] = item.text()
                    elif isinstance(item, QtWidgets.QCheckBox):
                        self.current_sro[key] = item.isChecked()
        
        self.config['screen_recorder_options'] = json.dumps(self.current_sro)

        self._set_current_config_values()


    def accept(self) -> None:
        
        self._get_current_config_values()

        #store config info on the local DB
        try:
            self.controller.save(self.config)
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Warning,
                                self.error_msg.TITLES['update_config_info'],
                                self.error_msg.MESSAGES['update_config_info'],
                                str(error)
                                )

            error_dlg.buttonClicked.connect(self.close)
            error_dlg.exec_()
        
        self.parent().reload_configuration()
        return super().accept()

    
    def reject(self) -> None:
        self.close()
        return super().reject()