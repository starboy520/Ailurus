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
import sys, os
from lib import *
from libapp import *

class _repo:
    @classmethod
    def exist(cls, path):
        import os
        return os.path.exists(path)
    @classmethod
    def enabled(cls, path):
        with open(path) as f:
            lines = f.readlines()
        return 'enabled=1\n' in lines
    @classmethod
    def enable(cls, path, only_enable_first_appearance = False):
        with open(path) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if lines[i].startswith('enabled='):
                lines[i] = 'enabled=1\n'
                if only_enable_first_appearance: break
        with TempOwn(path) as o:
            with open(path, 'w') as f:
                f.writelines(lines)
    @classmethod
    def disable(cls, path):
        with open(path) as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if lines[i].startswith('enabled='):
                lines[i] = 'enabled=0\n'
        with TempOwn(path) as o:
            with open(path, 'w') as f:
                f.writelines(lines)

class Repo_RPMFusion_Free:
    __doc__ = _('RPM Fusion (Free)')
    category = 'repository'
    detail = _('RPM Fusion provides software that not in the standard repositories.\n'
               'It is possible that "ATrpms" repository conflicts with "RPM Fusion" repository.')
    def __init__(self):
        self.paths = ['/etc/yum.repos.d/rpmfusion-free.repo', '/etc/yum.repos.d/rpmfusion-free-updates.repo']
    def installed(self):
        for path in self.paths:
           value = _repo.exist(path) and _repo.enabled(path)
           if not value: return False
        return True
    def install(self):
        all_exists = True
        for path in self.paths:
            if not _repo.exist(path):
                all_exists = False
        
        if all_exists:
            for path in self.paths:
                _repo.enable(path, only_enable_first_appearance = True)
        else:
            file = '/tmp/rpmfusion-free-release-stable.noarch.rpm'
            wget('http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm', file)
            RPM.install_local(file)
    def remove(self):
        for path in self.paths:
            if _repo.exist(path): _repo.disable(path)

class Repo_RPMFusion_NonFree:
    __doc__ = _('RPM Fusion (Non-Free)')
    category = 'repository'
    detail = _('RPM Fusion provides software that not in the standard repositories.')
    def __init__(self):
        self.paths = ['/etc/yum.repos.d/rpmfusion-nonfree.repo', '/etc/yum.repos.d/rpmfusion-nonfree-updates.repo']
    def installed(self):
        for path in self.paths:
           value = _repo.exist(path) and _repo.enabled(path)
           if not value: return False
        return True
    def install(self):
        all_exists = True
        for path in self.paths:
            if not _repo.exist(path):
                all_exists = False
        
        if all_exists:
            for path in self.paths:
                _repo.enable(path, only_enable_first_appearance = True)
        else:
            file = '/tmp/rpmfusion-nonfree-release-stable.noarch.rpm'
            wget('http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm', file)
            RPM.install_local(file)
    def remove(self):
        for path in self.paths:
            if _repo.exist(path): _repo.disable(path)

class Repo_Chromium(_repo):
    'Chromium'
    detail = _('Open source web browser')
    category = 'repository'
    def __init__(self):
        self.path = '/etc/yum.repos.d/chromium.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path):
            _repo.enable(self.path)
        else:
            with TempOwn(self.path) as o:
                with open(self.path, 'w') as f:
                    f.write('[chromium]\n'
                            'name=Chromium Test Packages\n'
                            'baseurl=http://spot.fedorapeople.org/chromium/F$releasever/\n'
                            'enabled=1\n'
                            'gpgcheck=0\n')
    def remove(self):
        if _repo.exist(self.path):
            _repo.disable(self.path)
