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
from applib import *

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
    

class Repo_Adobe:
    'Adobe'
    detail = _('This repository provides flash-plugin and Adobe Reader.')
    category = 'repository'
    def __init__(self):
        self.path = '/etc/yum.repos.d/adobe-linux-i386.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path):
            _repo.enable(self.path)
        else:
            file = '/tmp/adobe-release-i386-1.0-1.noarch.rpm'
            wget('http://linuxdownload.adobe.com/linux/i386/adobe-release-i386-1.0-1.noarch.rpm', file)
            RPM.install_local(file)
    def remove(self):
        if _repo.exist(self.path):
            _repo.disable(self.path)
    def support(self):
        return get_arch() == 32

class Repo_Skype:
    'Skype'
    category = 'repository'
    def __init__(self):
        self.path = '/etc/yum.repos.d/skype.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path):
            _repo.enable(self.path)
        else:
            with TempOwn(self.path) as o:
                with open(self.path, 'w') as f:
                    f.write('[skype]\n'
                        'name=Skype Repository\n'
                        'baseurl=http://download.skype.com/linux/repos/fedora/updates/i586/\n'
                        'enabled=1\n'
                        'gpgchek=0\n')
    def remove(self):
        if _repo.exist(self.path):
            _repo.disable(self.path)
    def support(self):
        return get_arch() == 32

class Repo_Livna:
    'Livna'
    category = 'repository'
    detail = _('It contains packages not available from the standard repositories.')
    def __init__(self):
        self.path = '/etc/yum.repos.d/livna.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path):
            _repo.enable(self.path, only_enable_first_appearance = True)
        else:
            file = '/tmp/livna-release.rpm'
            wget('http://rpm.livna.org/livna-release.rpm', file)
            RPM.install_local(file)
    def remove(self):
        if _repo.exist(self.path):
            _repo.disable(self.path)

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
    detail = _('RPM Fusion provides software that not in the standard repositories.\n'
               'It is possible that "ATrpms" repository conflicts with "RPM Fusion" repository.')
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

class Repo_ATrpms:
    'ATrpms'
    category = 'repository'
    detail = _('ATrpms is another third party repository.\n'
               'It is possible that "ATrpms" repository conflicts with "RPM Fusion" repository.')
    def __init__(self):
        self.path = '/etc/yum.repos.d/atrpms.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path): _repo.enable(self.path)
        else:
            with TempOwn(self.path) as o:
                with open(self.path, 'w') as f:
                    f.write('[ATrpms]\n'
                        'name=Fedora Core $releasever - $basearch - ATrpms\n'
                        'baseurl=http://dl.atrpms.net/f$releasever-$basearch/atrpms/stable\n'
                        'gpgkey=http://ATrpms.net/RPM-GPG-KEY.atrpms\n'
                        'gpgcheck=1\n'
                        'enabled=1\n')
    def remove(self):
        if _repo.exist(self.path): _repo.disable(self.path)

class Repo_Google:
    'Google'
    category = 'repository'
    detail = _('This repository provides Picasa and Google Desktop.')
    def __init__(self):
        self.path = '/etc/yum.repos.d/google.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path): _repo.enable(self.path, False)
        else:
            with TempOwn(self.path) as o:
                with open(self.path, 'w') as f:
                    f.write('[Google]\n'
                        'name=Google - i386\n'
                        'baseurl=http://dl.google.com/linux/rpm/stable/i386\n'
                        'enabled=1\n'
                        'gpgcheck=1\n'
                        '\n'
                        '[GoogleTesting]\n'
                        'name=Google Testing - i386\n'
                        'baseurl=http://dl.google.com/linux/rpm/testing/i386\n'
                        'enabled=1\n'
                        'gpgcheck=1\n')
            wget('https://dl-ssl.google.com/linux/linux_signing_key.pub', '/tmp/key.gpg')
            RPM.import_key('/tmp/key.gpg')
    def remove(self):
        if _repo.exist(self.path): _repo.disable(self.path)

class Repo_Google_Chrome:
    'Google Chrome'
    category = 'repository'
    detail = _('This repository provides Google Chrome.')
    def __init__(self):
        self.path = '/etc/yum.repos.d/google-chrome.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path): _repo.enable(self.path)
        else:
            with TempOwn(self.path) as o:
                if get_arch() == 32: arch = 'i386'
                else: arch = 'x86_64'
                
                with open(self.path, 'w') as f:
                    f.write('[google-chrome]\n'
                        'name=google-chrome\n'
                        'baseurl=http://dl.google.com/linux/rpm/stable/%s\n'
                        'enabled=1\n'
                        'gpgcheck=1\n'
                        'gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub\n' % arch
                        )
            wget('https://dl-ssl.google.com/linux/linux_signing_key.pub', '/tmp/key.gpg')
            RPM.import_key('/tmp/key.gpg')
    def remove(self):
        if _repo.exist(self.path): _repo.disable(self.path)

class Repo_VirtualBox:
    'VirtualBox'
    category = 'repository'
    logo = 'virtualbox.png'
    detail = _('This repository provides VirtualBox.\n'
               'Webpage: http://www.virtualbox.org/wiki/Linux_Downloads')
    def __init__(self):
        self.path = '/etc/yum.repos.d/virtualbox.repo'
    def installed(self):
        return _repo.exist(self.path) and _repo.enabled(self.path)
    def install(self):
        if _repo.exist(self.path): _repo.enable(self.path)
        else:
            with TempOwn(self.path) as o:
                with open(self.path, 'w') as f:
                    f.write('[virtualbox]\n'
                        'name=Fedora $releasever - $basearch - VirtualBox\n'
                        'baseurl=http://download.virtualbox.org/virtualbox/rpm/fedora/$releasever/$basearch\n'
                        'enabled=1\n'
                        'gpgcheck=1\n'
                        'gpgkey=http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc\n'
                        )
            wget('http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc', '/tmp/key.gpg')
            RPM.import_key('/tmp/key.gpg')
    def remove(self):
        if _repo.exist(self.path): _repo.disable(self.path)