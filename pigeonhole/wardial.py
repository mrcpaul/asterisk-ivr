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

"""AGI script that renders speech to text using Google Cloud Speech API
 using the REST API."""

# [START import_libraries]
from __future__ import print_function

from asterisk.agi import *
import re
import ConfigParser

from datetime import date, datetime, timedelta
import mysql.connector as mariadb

def question(file, valid_digits):
    regexp = re.compile(r'[' + valid_digits + ']')
    
    res = agi.get_data(file, 20000, 1)
    if regexp.search(res) is not None:
        return res

    res = agi.get_data(file, 20000, 1)    
    if regexp.search(res) is not None:
        return res
        
    if not res:
        agi.hangup()

settings = ConfigParser.RawConfigParser()
settings.read('/etc/asterisk/res_config_mysql.conf')

config = {
  'user': settings.get('general', 'dbuser'),
  'password': settings.get('general', 'dbpass'),
  'host': settings.get('general', 'dbhost'),
  'database': settings.get('general', 'dbname'),
  'raise_on_warnings': True,
}

def data_insert(query):                           
    agi.verbose(query)
    try:
        mariadb_connection = mariadb.connect(**config)
        cursor = mariadb_connection.cursor()
        cursor.execute(query)
        record = cursor.lastrowid
        mariadb_connection.commit()
        cursor.close()
        mariadb_connection.close()
    except mariadb.Error as error:
        agi.verbose("Database Error: {0}".format(error))
    return record

db_insert = ("INSERT INTO `warlist` (`clid`, `%s`) VALUES ('%s', '%s')")
db_update = ("UPDATE `warlist` SET `%s` = '%s' WHERE `id` = '%s'")

agi = AGI()
agi.answer()

clid = agi.env['agi_accountcode']

# Asterisk Dial-plan Application 'DumpChan()'
#Variables:
#WOMBAT_HOPPER_ID=2145573608
#warlist=38418
#NUM=
#SIPCALLID=1583cd9c69daeca70f5a91477e22f3b7@172.17.70.223:5060

wombat = agi.get_variable('WOMBAT_HOPPER_ID')
warlist = agi.get_variable('warlist')

agi.verbose("Database Record: {0}".format(warlist))

amdstatus = agi.env['agi_arg_2']
amdreason = agi.env['agi_arg_3']

if amdstatus == "MACHINE":
    agi.appexec('UserEvent', 'CALLSTATUS, UniqueID:%s,V:AMD' % wombat)
    data_insert(db_update % ('note', '%s:%s' % (amdstatus, amdreason), warlist))
    agi.hangup()

data_insert(db_update % ('note', '%s:%s' % (amdstatus, amdreason), warlist))

agi.stream_file('wardial/greeting')

q1 = question('wardial/question1', '12')
data_insert(db_update % ('q1', q1, warlist))

q2 = question('wardial/question2', '123')
data_insert(db_update % ('q2', q2, warlist))

q3 = question('wardial/question3', '12345')
data_insert(db_update % ('q3', q3, warlist))

q4 = question('wardial/question4', '123')
data_insert(db_update % ('q4', q4, warlist))

q5 = question('wardial/question5', '123')
data_insert(db_update % ('q5', q5, warlist))

agi.stream_file('wardial/goodby')

agi.hangup()

# calltime = agi.get_variable('ANSWEREDTIME')
# data_insert(db_update % ('reply', calltime, warlist))




