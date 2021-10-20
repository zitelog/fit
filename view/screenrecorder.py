#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: screenrecorder.py
# Project: FIT
# Created Date: Wednesday, July 28th 2021, 10:05:40 am
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

import pyautogui
import cv2
import numpy as np
import sys

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox


from view.error import ErrorView
from common.error import ErrorMessage


class ScreenRecorderView(QObject):
    finished = pyqtSignal()  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.error_msg = ErrorMessage()
        self.run = True
        self.destroyed.connect(self.stop)
        
    def set_options(self, options):
        # Specify resolution
        self.resolution = tuple(int(el) for el in options['resolution'])

        # Specify video codec
        self.codec = cv2.VideoWriter_fourcc(*options['codec'])

        # Specify frames rate. We can choose any
        # value and experiment with it
        self.fps = options['fps']

        # Specify name of Output file
        self.filename = options['filename']
        
    def start(self):
        # Creating a VideoWriter object
        self.out = cv2.VideoWriter(self.filename, self.codec, self.fps, self.resolution)
        try:
            while self.run:
                # Take screenshot using PyAutoGUI
                img = pyautogui.screenshot()

                # Convert the screenshot to a numpy array
                frame = np.array(img)

                # Convert it from BGR(Blue, Green, Red) to
                # RGB(Red, Green, Blue)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Write it to the output file
                self.out.write(frame)
        except:
                error_dlg = ErrorView(QMessageBox.Critical,
                            self.error_msg.TITLES['screen_recoder'],
                            self.error_msg.MESSAGES['screen_recoder'],
                            str(sys.exc_info()[0])
                            )

                error_dlg.buttonClicked.connect(quit)
                error_dlg.exec_()

        # Release the Video writer
        self.out.release()

        self.finished.emit()  # emit the finished signal when the loop is done
        # Destroy all windows
        cv2.destroyAllWindows()

    def stop(self):
        self.run = False  # set the run condition to false on stop 
