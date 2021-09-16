#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: web.py
# Project: FIT
# Created Date: Saturday, June 19th 2021, 8:27:36 am
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

import os
import sys
import json
import logging
import logging.config

#I don't know why but pywebcopy "original" (by Raja Tomar) hangs the console and does not exit.
#If I understood corretly this issue is knowed (https://github.com/rajatomar788/pywebcopy/issues/46)
#David W Grossman has found a workaround He removed all multithreading and commit this version 
# here https://github.com/davidwgrossman/pywebcopy. for this reason I used this "unofficial" version in the local lib path
from lib.pywebcopy import WebPage, config as pwc_config, core


from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets



from view.screenrecorder import ScreenRecorderView
from view.packetcapture import PacketCaptureView
from view.acquisitionstatus import AcquisitionStatusView

from view.case import CaseView
from view.configuration import ConfigurationView
from view.error import ErrorView

from controller.configuration import ConfigurationController
from controller.case import CaseController


from common.error import ErrorMessage

from common.settings import DEBUG
from common.config import LogConfig
import common.utility as utility

logger_acquisition = logging.getLogger(__name__)
logger_hashreport = logging.getLogger('hashreport')


class Screenshot(QtWebEngineWidgets.QWebEngineView):

    def capture(self, url, output_file):
        self.output_file = output_file
        self.load(QtCore.QUrl(url))
        self.loadFinished.connect(self.on_loaded)
        # Create hidden view without scrollbars
        self.setAttribute(QtCore.Qt.WA_DontShowOnScreen)
        self.page().settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.ShowScrollBars, False)
        self.show()

    def on_loaded(self):
        size = self.page().contentsSize().toSize()
        self.resize(size)
        # Wait for resize
        QtCore.QTimer.singleShot(1000, self.take_screenshot)

    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')
        self.close()


class WebView(QtWidgets.QMainWindow):

    stop_signal = QtCore.pyqtSignal()  # make a stop signal to communicate with the workers in another threads

    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(*args, **kwargs)
        self.error_msg = ErrorMessage()
        self.acquisition_directory = None
        self.acquisition_is_started = False
        self.acquisition_status =  AcquisitionStatusView()
        self.acquisition_status.setupUi()
        self.log_confing = LogConfig()
        self.is_enabled_screen_recorder = False
    
    def init(self, case_id):

        #To start the acquisition it is necessary the case information are present on the DB
        try:
           self.case_controller = CaseController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Critical,
                            self.error_msg.TITLES['acquisition'],
                            self.error_msg.MESSAGES['get_case_info'],
                            str(error)
                            )
                    
            error_dlg.buttonClicked.connect(quit)
            error_dlg.exec_()

        self.case_info = self.case_controller.get_case_from_id(case_id)
        if not self.case_info:
            error = 'Case ID: ' + str(case_id) + ' was not found on the DB'
            error_dlg = ErrorView(QtWidgets.QMessageBox.Critical,
                              self.error_msg.TITLES['acquisition'],
                              self.error_msg.MESSAGES['get_case_id'],
                              error
                              )
            error_dlg.buttonClicked.connect(quit)
            error_dlg.exec_()

        #To start the acquisition it is also necessary load the configuration information from the DB
        try:
            config_controller = ConfigurationController()
        except Exception as error:
            error_dlg = ErrorView(QtWidgets.QMessageBox.Critical,
                                self.error_msg.TITLES['acquisition'],
                                self.error_msg.MESSAGES['get_configuration'],
                                str(error)
                                )

            error_dlg.buttonClicked.connect(quit)
            error_dlg.exec_()

        self.config = config_controller.get_configuration()
       

        
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)



        self.setCentralWidget(self.tabs)

        self.status = QtWidgets.QStatusBar()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMaximumWidth(400)
        self.progress_bar.setFixedHeight(25)
        self.status.addPermanentWidget(self.progress_bar)
        
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.setStatusBar(self.status)
        self.progress_bar.setHidden(True)

        


        navtb = QtWidgets.QToolBar("Navigation")
        navtb.setObjectName('NavigationToolBar')
        navtb.setIconSize(QtCore.QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.back())
        navtb.addAction(back_btn)

        next_btn = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'arrow-000.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.forward())
        navtb.addAction(next_btn)

        reload_btn = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'arrow-circle-315.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.reload())
        navtb.addAction(reload_btn)

        home_btn = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QtWidgets.QLabel()  # Yes, really!
        self.httpsicon.setPixmap(QtGui.QPixmap(os.path.join('asset/images', 'lock-nossl.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QtWidgets.QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'cross-circle.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # Uncomment to disable native menubar on Mac
        self.menuBar().setNativeMenuBar(False)

        tab_menu = self.menuBar().addMenu("&Tab")
        new_tab_action = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'ui-tab--plus.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        tab_menu.addAction(new_tab_action)

        #ACQUISITION MENU
        acquisition_menu = self.menuBar().addMenu("&Acquisition")

        start_acquisition_action = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'start.png')), "Start", self)
        start_acquisition_action.setObjectName('StartAcquisitionAction')
        start_acquisition_action.triggered.connect(self.start_acquisition)
        acquisition_menu.addAction(start_acquisition_action)
        stop_acquisition_action = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'stop.png')), "Stop", self)
        stop_acquisition_action.setObjectName('StopAcquisitionAction')
        stop_acquisition_action.triggered.connect(self.stop_acquisition)
        acquisition_menu.addAction(stop_acquisition_action)
        acquisition_status_action = QtWidgets.QAction(QtGui.QIcon(os.path.join('asset/images', 'stop.png')), "Status", self)
        acquisition_status_action.setObjectName('StatusAcquisitionAction')
        acquisition_status_action.triggered.connect(self._acquisition_status)
        acquisition_menu.addAction(acquisition_status_action)

        #CASE ACTION
        case_action = QtWidgets.QAction("Case", self)
        case_action.setStatusTip("Show case info")
        case_action.triggered.connect(self.case)
        self.menuBar().addAction(case_action)

        #CONFIGURATION ACTION
        configuration_action = QtWidgets.QAction("Configuration", self)
        configuration_action.setStatusTip("Show configuration info")
        configuration_action.triggered.connect(self.configuration)
        self.menuBar().addAction(configuration_action)



        self.add_new_tab(QtCore.QUrl(self.config['home_page_url']), 'Homepage')

        self.show()

        self.setWindowTitle("Freezing Internet Tool")
        self.setWindowIcon(QtGui.QIcon(os.path.join('asset/images/', 'icon.png')))

        #Enable/Disable other modules logger
        if not DEBUG:
            loggers = [logging.getLogger()]  # get the root logger
            loggers = loggers + [logging.getLogger(name) for name in  logging.root.manager.loggerDict if name not in [__name__ , 'hashreport'] ]

            self.log_confing.disable_loggers(loggers)

    def start_acquisition(self):
        
        # Step 1: Disable start_acquisition_action and clear current threads and acquisition information on dialog
        action = self.findChild(QtWidgets.QAction, 'StartAcquisitionAction')
        self.progress_bar.setValue(50)
        if action is not None:
            action.setEnabled(False)
        
        
        self.acquisition_status.clear()
        self.acquisition_status.set_title('Acquisition is started!')
       
        # Step 2: Create acquisiton directory
        self.acquisition_directory = self.case_controller.create_acquisition_directory(
                                                    'web', 
                                                    self.config, 
                                                    self.case_info, 
                                                    self.tabs.currentWidget().url().toString()
                                                    )
        if self.acquisition_directory is not None:

            #show progress bar
            self.progress_bar.setHidden(False)

            self.acquisition_is_started = True
            self.acquisition_status.set_title('Acquisition in progress:')
            self.acquisition_status.add_task('Case Folder')
            self.acquisition_status.set_status('Case Folder', self.acquisition_directory, 'done')
            self.status.showMessage(self.acquisition_directory)
            self.progress_bar.setValue(25)

            #Step 3: Create loggin handler and start loggin information
            self.log_confing.change_filehandlers_path(self.acquisition_directory)
            logging.config.dictConfig(self.log_confing.config)
            logger_acquisition.info('Acquisition started')
            self.acquisition_status.add_task('Logger')
            self.acquisition_status.set_status('Logger', 'Started', 'done')
            self.status.showMessage('Logging handler and login information have been started')
            self.progress_bar.setValue(50)

            #Step 4: Add new thread for network packet capture and start it
            options = {'acquisition_directory': self.acquisition_directory, 'filename' : 'acquisition.pcap'}
            self.start_packet_capture(options)
            self.acquisition_status.add_task('Network Packet Capture')
            self.acquisition_status.set_status('Network Packet Capture', 'Capture loop has been starded in a new thread!', 'done')
            logger_acquisition.info('Network Packet Capture started')
            self.status.showMessage('Capture loop has been starded in a new thread!')
            self.progress_bar.setValue(75)

            #Step 5: Add new thread for screen video recoder and start it
            options = json.loads(self.config['screen_recorder_options'])
            self.is_enabled_screen_recorder = bool(options['enabled'])

            if self.is_enabled_screen_recorder:
                options['filename'] = os.path.join(self.acquisition_directory, options['filename'])
                self.start_screen_recoder(options)
                self.acquisition_status.add_task('Screen Recoder')
                self.acquisition_status.set_status('Screen Recoder', 'Recoder loop has been starded in a new thread!', 'done')
                self.status.showMessage('Recoder loop has been starded in a new thread!')
                self.progress_bar.setValue(100)
                logger_acquisition.info('Screen recoder started')
                logger_acquisition.info('Initial URL: ' + self.tabs.currentWidget().url().toString())
                self.acquisition_status.set_title('Acquisition started success:')

            #hidden progress bar
            self.progress_bar.setHidden(True)
            self.status.showMessage('')
    
    def stop_acquisition(self):
   

        if self.acquisition_is_started:
            self.progress_bar.setHidden(False)
        
            #Step 1: Disable all actions and clear current acquisition information on dialog
            self.setEnabled(False)
            self.acquisition_status.clear()
            self.acquisition_status.set_title('Interruption of the acquisition in progress:')
            logger_acquisition.info('Acquisition stopped')
            logger_acquisition.info('End URL: ' + self.tabs.currentWidget().url().toString())
            self.statusBar().showMessage('Message in statusbar.')
            #Step 2: stop threads 
            self.packetcapture.stop()

            if self.is_enabled_screen_recorder:
                self.screenrecorder.stop()

            #Step 3:  Save screenshot of current page
            self.status.showMessage('Save screenshot of current page')
            self.progress_bar.setValue(10)
            logger_acquisition.info('Save screenshot of current page')
            screenshot = Screenshot()
            screenshot.capture(self.tabs.currentWidget().url().toString(), 
                               os.path.join(self.acquisition_directory, 'screenshot.png'))

            
            self.acquisition_status.add_task('Screenshot Page')
            self.acquisition_status.set_status('ScreenShot Page', 'Screenshot of current web page is done!', 'done')

           

            self.status.showMessage('Save all resource of current page')
            self.progress_bar.setValue(20)
            #Step 4:  Save all resource of current page
            zip_folder = None
            if self.save_page():
               zip_folder = core.zip_project()
            
            logger_acquisition.info('Save all resource of current page')
            self.acquisition_status.add_task('Save Page')
            self.acquisition_status.set_status('Save Page',zip_folder, 'done')
           

            ### Waiting everything is synchronized  
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(2000, loop.quit)
            loop.exec_()
   
            self.status.showMessage('Calculate acquisition file hash')
            self.progress_bar.setValue(100)
            #Step 5:  Calculate acquisition hash
            logger_acquisition.info('Calculate acquisition file hash')
            files = [ f.name for f in os.scandir(self.acquisition_directory) if f.is_file() ]

            for file in files:
                filename = os.path.join(self.acquisition_directory, file)
                file_stats = os.stat(filename)
                logger_hashreport.info(file)
                logger_hashreport.info('=========================================================')
                logger_hashreport.info(f'Size: {file_stats.st_size}')
                algorithm = 'md5'
                logger_hashreport.info(f'MD5: {utility.calculate_hash(filename, algorithm)}')
                algorithm = 'sha1'
                logger_hashreport.info(f'SHA-1: {utility.calculate_hash(filename, algorithm)}')
                algorithm = 'sha256'
                logger_hashreport.info(f'SHA-256: {utility.calculate_hash(filename, algorithm)}')

        #     #TODO Step 6: calulate FIT hash 
        #     logger_acquisition.info('Calculate FIT hash')
              

            logger_acquisition.info('Acquisition end')

            #### open the acquisition folder ####
            QtWidgets.QFileDialog.getOpenFileName(None, 'Acquisition Case Folder', self.acquisition_directory, 'All Files(*.*)')

            #### Enable all action ####
            self.setEnabled(True)
            action = self.findChild(QtWidgets.QAction, 'StartAcquisitionAction')
            
            #Enable start_acquisition_action
            if action is not None:
                action.setEnabled(True)

            self.acquisition_is_started = False

            #hidden progress bar
            self.progress_bar.setHidden(True)
            self.status.showMessage('')
            
    def _acquisition_status(self):
        self.acquisition_status.show()

    def start_packet_capture(self, options):
        
        self.th_packetcapture = QtCore.QThread()

        self.packetcapture = PacketCaptureView()
        self.packetcapture.set_options(options)

        self.packetcapture.moveToThread(self.th_packetcapture)

        self.th_packetcapture.started.connect(self.packetcapture.start)
        self.packetcapture.finished.connect(self.th_packetcapture.quit)
        self.packetcapture.finished.connect(self.packetcapture.deleteLater)
        self.th_packetcapture.finished.connect(self.th_packetcapture.deleteLater)
        self.th_packetcapture.finished.connect(self._thread_packetcapture_is_finished)

        self.th_packetcapture.start()

    def _thread_packetcapture_is_finished(self):
        self.status.showMessage('Loop has been stopped and .pcap file has been saved in the case folder')
        value = self.progress_bar.value() + 30
        self.progress_bar.setValue(value)
        logger_acquisition.info('Network Packet Capture stopped')
        self.acquisition_status.add_task('Network Packet Capture')
        self.acquisition_status.set_status('Network Packet Capture', 'Loop has been stopped and .pcap file has been saved in the case folder', 'done')
        self.th_packetcapture.quit()
        self.th_packetcapture.wait()
    
       

    def start_screen_recoder(self, options):
        self.th_screenrecorder = QtCore.QThread()

        self.screenrecorder = ScreenRecorderView()
        self.screenrecorder.set_options(options)

        self.screenrecorder.moveToThread(self.th_screenrecorder)
 
        self.th_screenrecorder.started.connect(self.screenrecorder.start)
        self.screenrecorder.finished.connect(self.th_screenrecorder.quit)
        self.screenrecorder.finished.connect(self.screenrecorder.deleteLater)
        self.th_screenrecorder.finished.connect(self.th_screenrecorder.deleteLater)
        self.th_screenrecorder.finished.connect(self._thread_screenrecorder_is_finished)
  
        self.th_screenrecorder.start()
    
    def _thread_screenrecorder_is_finished(self):
        self.status.showMessage('Loop has been stopped and .avi file has been saved in the case folder')
        value = self.progress_bar.value() + 30
        self.progress_bar.setValue(value)
        logger_acquisition.info('Screen recoder stopped')
        self.acquisition_status.add_task('Screen Recoder')
        self.acquisition_status.set_status('Screen Recoder', 'Loop has been stopped and .avi file has been saved in the case folder', 'done')
        self.th_screenrecorder.quit()
        self.th_screenrecorder.wait()


    def save_page(self):

        url = self.tabs.currentWidget().url().toString()

        pwc_config.setup_config(
            project_url=url,
            project_folder=self.acquisition_directory,
            project_name='acquisition_page',
            over_write=True,
            bypass_robots=True,
            delete_project_folder=True
        )

        # Create a instance of the webpage object
        wp = WebPage()
        # If you want to use `requests` to fetch the page then
        wp.get(url)
        wp.save_complete()

        # location of the html file written 
        return wp.file_path

    def case(self):
        form = CaseView(self.case_info)
        form.exec_()
    
    def configuration(self):
        config = ConfigurationView()
        config.exec_()


    def back(self):
        if self.acquisition_is_started:
            logger_acquisition.info('User clicked the back button')
        self.tabs.currentWidget().back()
        
    
    def forward(self):
        if self.acquisition_is_started:
            logger_acquisition.info('User clicked the forward button')
        self.tabs.currentWidget().forward()
        
    
    def reload(self):
        if self.acquisition_is_started:
            logger_acquisition.info('User clicked the reload button')
        self.tabs.currentWidget().reload()
       
        
    def add_new_tab(self, qurl=None, label="Blank"):
        if self.acquisition_is_started:
            logger_acquisition.info('User add new tab')

        if qurl is None:
            qurl = QtCore.QUrl('')

        browser = QtWebEngineWidgets.QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)
        

        # More difficult! We only want to update the url when it's from the
        # correct tab
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadProgress.connect(self.load_progress)

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

        if i == 0:
            self.showMaximized()
        

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.acquisition_is_started:
            logger_acquisition.info('User remove tab')
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Freezing Internet Tool" % title)


    def navigate_home(self):
        if self.acquisition_is_started:
            logger_acquisition.info('User clicked the home button')

        self.tabs.currentWidget().setUrl(QtCore.QUrl(self.config['home_page_url']))

    def navigate_to_url(self):  # Does not receive the Url
        q = QtCore.QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        
        self.tabs.currentWidget().setUrl(q)

    def load_progress(self, prog):
        if self.acquisition_is_started and prog == 100:
            logger_acquisition.info('Loaded: ' + self.tabs.currentWidget().url().toString())

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return

        if q.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QtGui.QPixmap(os.path.join('asset/images', 'lock-ssl.png')))

        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QtGui.QPixmap(os.path.join('asset/images', 'lock-nossl.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def closeEvent(self, event):
        packetcapture = getattr(self, 'packetcapture', None)

        if packetcapture is not None:
            packetcapture.stop()
        
