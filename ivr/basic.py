#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# Copyright 2016 INVITE Communications Co., Ltd. All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Asterisk Configuration File
######################################################
This module is used to read the database settings from an Asterisk configuration file.  It uses the Python ConfigParser to load the setting values directly from the specified section (context) of the Asterisk configuration file.

.. note:: You need the `MySQL Connector/Python <https://dev.mysql.com/downloads/connector/python/>`_ installed on your system to connect to the database.

Example:
    Import the module, get the config settings, and pass them to your mysql connection::

        import ivr.connection
        config = ivr.connection.config
        database = mysql.connect(**config)

"""

from asterisk.agi import *
from distutils.util import strtobool

agi = AGI()
agi.answer()

try:
    """
    Check AMD dialplan variable for affirmitive setting.
    Variables evaluated in the dialplan are case-insensitive.
    
    Set(AMD = true)
    
    True values are y, yes, t, true, on and 1; 
    false values are n, no, f, false, off and 0. 
    Raises ValueError if val is anything else.
    
    When the dialpaln variable is not set, ValueError is ignored.
    """
    if(strtobool(agi.get_variable('amd'))):
        agi.appexec('AMD')
        amdstatus = agi.get_variable('AMDSTATUS')
        amdcause = agi.get_variable('AMDCAUSE')
        agi.verbose('AMD Status: {0} Cause: {1}'.format(amdstatus, amdcause))
    else:
        agi.verbose('AMD Disabled')
except ValueError:
    agi.verbose('NOTICE: AMD Dialplan Variable NOT Set!',2)
    pass
    


#variable = agi.get_variable('variable')
#env = agi.env['agi_arg_1']
#agi.appexec('DumpChan')

agi.stream_file('tt-monty-knights')

agi.hangup()