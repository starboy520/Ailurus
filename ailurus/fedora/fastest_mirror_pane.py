#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Ailurus - make Linux easier to use
#
# Copyright (C) 2007-2010, Trusted Digital Technology Laboratory, Shanghai Jiao Tong University, China.
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
import gtk, pango
import sys, os
from lib import *
from libu import *
from libserver import *

class FedoraFastestMirrorPane(gtk.VBox):
    name = _('Find fastest repository mirror')

    COUNTRY = 0
    ORG = 1
    URL = 2
    RESPONSE_TIME = 3
    NO_PING_RESPONSE = 10000
    
    def __init__(self, main_view):
        assert hasattr(main_view, 'lock')
        assert hasattr(main_view, 'unlock')
        self.main_view = main_view
        
        gtk.VBox.__init__(self, False, 5)

if __name__ == '__main__':
    path = Config.get_config_dir() + 'response_time_2'
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write('a\n1\nb\n2\n')
    ResponseTime.load()
    print ResponseTime.map
    ResponseTime.set('b', 3)
    