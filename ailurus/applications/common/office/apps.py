#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
# Copyright (C) 2009-2010, Ailurus Developers Team
#
# Ailurus is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ailurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ailurus; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from __future__ import with_statement
import sys, os
from lib import *
from libapp import *

class Evince_Read_Chinese_PDF(_rpm_install) :
    __doc__ = _('Make Evince be able to reveal Chinese, Japanese, Korean pdf')
    category='office'
    if FEDORA:
        pkgs = 'poppler-data'

class CHMSee_Read_CHM_Documents(_rpm_install) :
    __doc__ = _('ChmSee: A CHM file viewer')
    category = 'office'
    license = GPL + ' http://code.google.com/p/chmsee/'
    if FEDORA:
        pkgs = 'chmsee'

class CUPS (_rpm_install):
    __doc__ = _('Enable "Print to pdf" capability.')
    category = 'office'
    if FEDORA:
        pkgs = 'cups-pdf'

class Stardict_without_Dictionaries(_rpm_install):
    __doc__ = _('Stardict')
    category = 'office'
    detail = _('You can install these dictionaries by yum.\n'
               'stardict-dic-cs_CZ: Czech dictionaries\n'
               'stardict-dic-en: English dictionaries\n'
               'stardict-dic-hi: Hindi dictionary\n'
               'stardict-dic-ja: Japanese dictionaries\n'
               'stardict-dic-ru: Russian dictionaries\n'
               'stardict-dic-zh_CN: Simplified Chinese dictionaries\n'
               'stardict-dic-zh_TW: Traditional Chinese dictionaries')
    license = GPL
    if FEDORA:
        pkgs = 'stardict'

