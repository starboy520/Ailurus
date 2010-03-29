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

import gtk
import sys
import os
from lib import *

class CleanUpPane(gtk.HBox):
    name = _('Clean up')
    
    def __init__(self, main_view):
        gtk.HBox.__init__(self, False, 5)
        vbox = self.rightpane = gtk.VBox()
        clean_cache = CleanCache()
        clean_kernel = CleanKernel()
        vbox.pack_start(clean_cache)
        vbox.pack_start(clean_kernel)
        self.pack_start(vbox)

class CleanCache(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.cache_path = '/var/cache/ailurus'
        desc = gtk.Label(_('size of %s: %s')%(self.cache_path, self.__get_cache_size()))
        clnbtn = gtk.Button(_('Clean'))
        def __clean_up(*w):
            print 'cleaning'
            gksudo('rm -rf %s/*; apt-get clean'%self.cache_path)
        clnbtn.connect('clicked', __clean_up)
        self.pack_start(desc)
        self.pack_start(clnbtn)
        
    def __get_cache_size(self):
        try:
            size = get_output('du -bs %s'%self.cache_path)
            size = int(size.split('\t', 1)[0])
        except:
            size = 0
            import traceback
            traceback.print_exc(file=sys.stderr)
        return derive_size(size)

class CleanKernel(gtk.VBox):
    def __init__(self):
        import re
        
        gtk.VBox.__init__(self)
        self.current_kernel_version = os.uname()[2]
        print 'current: %s'%self.current_kernel_version
        clnbtn = gtk.Button(_('Clean unused kernel'))
        def __clean_up(*w):
            generic = 'generic'
            headers_pattern = r'linux-headers-(.+)'
            image_pattern = r'linux-image-(.+)'
            remove_list = []
            pkgs = APT.get_installed_pkgs_set()
            headers_set = [p for p in pkgs if p.startswith('linux-headers-')]
            image_set = [p for p in pkgs if p.startswith('linux-image-')]
            for p in headers_set:
                match = re.search(headers_pattern, p)
                if match:
                    version = match.group(1)
                else:
                    continue
                if not (version == self.current_kernel_version or version == generic):
                    remove_list.append(p)
            for p in image_set:
                match = re.search(image_pattern, p)
                if match:
                    version = match.group(1)
                else:
                    continue
                if not (version == self.current_kernel_version or version == generic):
                    remove_list.append(p)
            for p in remove_list: print p
        clnbtn.connect('clicked', __clean_up)
        self.pack_start(clnbtn)
        