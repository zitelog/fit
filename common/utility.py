#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: utility.py
# Project: FIT
# Created Date: Tuesday, July 27th 2021, 12:48:05 pm
# Author: Fabio Zito
# -----
# Last Modified: Fri Sep 03 2021
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



import sys
import winreg
import hashlib

def get_platform():

    platforms = {
        'linux1' : 'lin',
        'linux2' : 'lin',
        'darwin' : 'osx',
        'win32'  : 'win'
    }

    if sys.platform not in platforms:
        return 'other'

    return platforms[sys.platform]

def get_list_of_programs_installed_on_windows(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list

def program_is_installed(name):
    program = None
    is_istalled = False
    software_list = None
    if get_platform() == 'win':
        software_list = get_list_of_programs_installed_on_windows(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + \
                        get_list_of_programs_installed_on_windows(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + \
                        get_list_of_programs_installed_on_windows(winreg.HKEY_CURRENT_USER, 0)
    
    if software_list is not None:
        for software in software_list:
            if name in software['name']:
                program = {'name':software['name'], 'version':software['version'], 'publisher':software['publisher']}
                is_istalled = True
                break

    return is_istalled

def calculate_hash(filename, algorithm):
    with open(filename, "rb") as f:
        file_hash = hashlib.new(algorithm)
        while chunk := f.read(8192):
            file_hash.update(chunk)

        return file_hash.hexdigest()
