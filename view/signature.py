#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: mrhasher.py
# Project: FIT
# Created Date: Wednesday, July 28th 2021, 10:05:40 am
# Author: Fabio Zito
# -----
# Last Modified: Sun Oct 24 2021
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
import platform
import logging
import json
import re

from datetime import datetime

logging.basicConfig(format='%(levelname)s:%(asctime)s - %(message)s', level=logging.DEBUG, datefmt='%d/%m/%Y %I:%M:%S %p')

from PyQt5.QtCore import QObject, pyqtSignal, QProcess, QFile, QFileInfo, Qt, QDateTime
from PyQt5.QtWidgets import QMessageBox, QFileDialog


from view.error import ErrorView

from controller.configuration import ConfigurationController

from common.error import ErrorMessage

import common.utility as utility

from common.settings import DEBUG, MAKE_REQUEST, CHECK_REQUEST

class SignatureView(QObject):

    finished = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.error_msg = ErrorMessage()
        #To start the acquisition it is also necessary load the configuration information from the DB
        try:
            self.config_controller = ConfigurationController()
        except Exception as error:
            error_dlg = ErrorView(QMessageBox.Critical,
                                self.error_msg.TITLES['acquisition'],
                                self.error_msg.MESSAGES['get_configuration'],
                                str(error)
                                )

            error_dlg.buttonClicked.connect(quit)
            error_dlg.exec_()

        self.config = self.config_controller.get_configuration()
        self.options = json.loads(self.config['signature_options'])

        self.p = None
        self.program = None
        self.arguments = None
        self.request = None
        self.signature_folder = None
        self.filename = 'signature'
    
    def __message_answer(self, answer):
        
        title = "Signature Result"
        display_message = None
        icon = None
        author  = 'Fabio Zito'
        date = ''
        id = ''
        if self.request == MAKE_REQUEST:
            if answer == 'signaturegenerated':
                with open(os.path.join(self.signature_folder, self.filename), encoding='utf8') as f:
                    for line in f:
                        if "clientChallenge" in line:
                            start = line.find(": \"") + len(": \"")
                            end = line.find("\",")
                            id = line[start:end]
                        elif "epoch" in line:
                            date = datetime.fromtimestamp(int(line.split(":")[1].strip())/1000).strftime("%Y-%m-%d %H:%M:%S %z")
                display_message = 'Signature was successfully generated:<br> Author: {}<br>Date: {}<br>Client challenge: {}'.format(author, date, id)   
                icon = QMessageBox.Information
            
            elif  answer == 'signature-file-already-exist':
                display_message = 'Signature file already exist in the directory:<br>({})'.format(self.options['acquisiton_directory'])
                icon = QMessageBox.Warning

            elif  answer == 'samesignature':
                display_message = 'You can\'t put a signature on the ({}) because already exists a signature in the path and <strong><u>it\'s the same</u></strong> as that of the server'.format(self.signature_folder)
                icon = QMessageBox.Warning
                
            elif answer == "alreadyexists":
                display_message = 'You can\'t put a signature on the ({}) because already exists a signature in the path and <strong><u>it is not the same</u></strong> as that of the server'.format(self.signature_folder)
                icon = QMessageBox.Critical
            else:
                display_message = 'Unexpected error see bellow for more detail:<br><br>' + answer
                icon = QMessageBox.Critical

        elif self.request == CHECK_REQUEST:
            if  answer == 'signature-file-not-exist':
                display_message = 'Signature file doesn\'t exist in the directory:<br>({})'.format(self.options['acquisiton_directory'])
                icon = QMessageBox.Critical

            elif  answer == 'samesignature':
                with open(os.path.join(self.signature_folder, self.filename), encoding='utf8') as f:
                    for line in f:
                        if "clientChallenge" in line:
                            start = line.find(": \"") + len(": \"")
                            end = line.find("\",")
                            id = line[start:end]
                        elif "epoch" in line:
                            date = datetime.fromtimestamp(int(line.split(":")[1].strip())/1000).strftime("%Y-%m-%d %H:%M:%S %z")

               
                display_message = 'In {} <strong><u>there is a valide signature</u></strong>:<br> Author: {}<br>Date: {}<br>Client challenge: {}'.format(self.signature_folder, author, date, id)
                icon = QMessageBox.Information

            elif answer == "invalidstatuscodedifferentsignature":
                display_message = 'In {} exists a signature, but <strong><u>it is not the same</u></strong> as that of the server'.format(self.signature_folder)
                icon = QMessageBox.Critical
            else:
                display_message = 'Unexpected error see bellow for more detail:<br><br>' + answer
                icon = QMessageBox.Critical

            

        dlg = QMessageBox(self.parent())
        dlg.setTextFormat(Qt.RichText)
        dlg.setWindowTitle(title)
        dlg.setText(display_message)
        dlg.setIcon(icon)

        dlg.exec()
    
    def generate(self, acquisiton_directory):
        self.request = MAKE_REQUEST

        #Silent mode
        if acquisiton_directory and os.path.exists(acquisiton_directory):
             self.options['acquisiton_directory'] = acquisiton_directory
        else: 
            if self.__waring_message() == QMessageBox.Yes:
                self.options['acquisiton_directory'] = self.__select_acquisition_directory()
        
        print(self.options['acquisiton_directory'])
        
        if 'acquisiton_directory' in self.options and self.options['acquisiton_directory']:    
            fileinfo = QFileInfo(os.path.join(self.options['acquisiton_directory'], self.filename))
            
            if fileinfo.exists():
                self.__message_answer("signature-file-already-exist")
            else:
                if self.__mrsign_configuration_options():
                    self.__start_process()
    
    def verify(self, acquisiton_directory):
        self.request = CHECK_REQUEST
        self.options['acquisiton_directory'] = acquisiton_directory
        fileinfo = QFileInfo(os.path.join(self.options['acquisiton_directory'], self.filename))

        if not fileinfo.exists():
            self.__message_answer("signature-file-not-exist")
        else:
            if self.__mrsign_configuration_options():
                self.__start_process()
        
    def __mrsign_configuration_options(self):
        
        are_ok_configuration_options = True

        
        fileinfo = QFileInfo(self.options['executable'])

        #Check 1: mrsign file exists
        if not fileinfo.exists():
            error_dlg = ErrorView(QMessageBox.Critical,
                                self.error_msg.TITLES['mrsign_configuration_options'],
                                self.error_msg.MESSAGES['mrsign_path'].format(self.options['executable']),
                                ''
                                )
            error_dlg.exec_()

            are_ok_configuration_options = False

        #Check 2: mrsign file is executable
        if are_ok_configuration_options and not fileinfo.isExecutable():
    
            error_dlg = ErrorView(QMessageBox.Critical,
                                self.error_msg.TITLES['mrsign_configuration_options'],
                                self.error_msg.MESSAGES['mrsign_executable'].format(self.options['executable']),
                                ''
                                )
            error_dlg.exec_()

            are_ok_configuration_options = False
            
        #Check 3: mrsign hostname and port   
        if are_ok_configuration_options:
            if not self.options['hostname'] or not self.options['port']:
                error_dlg = ErrorView(QMessageBox.Critical,
                                    self.error_msg.TITLES['mrsign_configuration_options'],
                                    self.error_msg.MESSAGES['mrsign_hostname_or_port'].format(self.options['executable']),
                                    ''
                                    )
                error_dlg.exec_()

                are_ok_configuration_options = False

        #Check 4: mrsign username and password TODO for autentication on the server 
        if are_ok_configuration_options:
            if not self.options['username'] or not self.options['password']:
                error_dlg = ErrorView(QMessageBox.Critical,
                                    self.error_msg.TITLES['mrsign_configuration_options'],
                                    self.error_msg.MESSAGES['mrsign_username_or_password'].format(self.options['executable']),
                                    ''
                                    )
                error_dlg.exec_()

                are_ok_configuration_options = False
        

        if are_ok_configuration_options:    
            os_username = os.getlogin()
            hostname = platform.node()
         
            server_store_path = 'mrsign/server' #TODO is a remote path remove this part of code
            challengeurl = self.options['protocol'] + '://' + self.options['hostname'] + ':' + str(self.options['port'])
            self.signature_folder = self.options['acquisiton_directory']
            
            self.program = self.options['executable']
            self.arguments = ['-t', hostname, '-u', os_username, '-r', challengeurl, '-p', self.options['acquisiton_directory'], 
                '-f',  self.filename, '-sp', server_store_path]

        return are_ok_configuration_options

    def __start_process(self):
        #START mrsign
        #TODO the mrsignserver starts in the local environment just for the developing test. 
        # In the production environment the server will be located in remote position and this part of code will be removed 
        utility.start_mrsign_sever(self.program)

        if self.p is None:  # No process running.
            if DEBUG:
                logging.debug("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.__handle_stdout)
            self.p.readyReadStandardError.connect(self.__handle_stderr)
            self.p.stateChanged.connect(self.__handle_state)
            self.p.finished.connect(self.__process_finished)  # Clean up once complete.
            self.p.start(self.program, self.arguments)
    
    def __waring_message(self):

        dlg = QMessageBox(self.parent())
        dlg.setWindowTitle("Signature Allert")
        dlg.setText("Putting a signature on the acquisiton, it means that the acquisition is burned.\
                    \n\nTherefore it will not be possible to put a new signature on the same acquisition neither if it is deleted and acquisited again.\
                    \n\nSo before proceeding you must be sure that this is your definitive acquisition. Do you want to continue?")
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dlg.setIcon(QMessageBox.Warning)

        return dlg.exec()

        
    
    def __select_acquisition_directory(self):
        folderpath = QFileDialog.getExistingDirectory(self.parent(), 'Select Acquisition Folder', os.path.expanduser(self.config['cases_folder_' + utility.get_platform()]))
        return folderpath



    def __handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")

        logging.warning(stderr)

    def __handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")

        if DEBUG:
            logging.debug(stdout)

        
        self.__message_answer(re.sub('\W+','', stdout).lower())

    def __handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]

        if DEBUG:
            logging.debug(f"State changed: {state_name}")

    def __process_finished(self):
        if DEBUG:
            logging.debug("Process finished.")

        self.p = None

        #STOP mrsign
        #TODO the mrsignserver starts in the local environment just for the developing test. 
        # In the production environment the server will be located in remote position and this part of code will be removed 
        utility.stop_mrsign_sever()


        self.finished.emit()
