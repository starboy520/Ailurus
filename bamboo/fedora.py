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
from ailurus.lib import *
from ailurus.libapp import *

if not Config.is_Fedora():
    raise Exception

class _repo:
    this_class_is_a_repository = True
    category = 'repository'
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

class GStreamer_Codecs (_rpm_install) :
    __doc__ = _('Multi-media codec')
    detail = _(
       'Command: yum install '
       'gstreamer gstreamer-plugins-bad gstreamer-plugins-bad-extras gstreamer-plugins-base'
                     'gstreamer-plugins-good gstreamer-plugins-ugly')
    category = 'media'
    logo = 'codec.png'
    depends = Repo_RPMFusion_Free
    pkgs = ('gstreamer gstreamer-plugins-bad gstreamer-plugins-bad-extras gstreamer-plugins-base'
            'gstreamer-plugins-good gstreamer-plugins-ugly')

class Adobe_Flash_Player(_rpm_install):
    __doc__ = _(u'Adobe® Flash plugin for web browser')
    detail = _('Command: yum install flash-plugin')
    category = 'media'
    logo = 'flash.png'
    depends = Repo_Adobe
    pkgs = 'flash-plugin'

class AdobeReader(_rpm_install):
    __doc__ = _(u'Adobe® PDF Reader')
    detail = _('Official site: http://get.adobe.com/cn/reader/')
    category = 'office'
    logo = 'adobereader.png'
    depends = Repo_Adobe
    def __init__(self):
        package_dict = {
                   'zh_HK':'AdobeReader_cht',
                   'zh_TW':'AdobeReader_cht',
                   'zh_CN':'AdobeReader_chs',
                   'de':'AdobeReader_deu',
                   'en':'AdobeReader_enu',
                   'es':'AdobeReader_esp',
                   'it':'AdobeReader_ita',
                   'nl':'AdobeReader_nld',
                   'pt':'AdobeReader_ptb',
                   }
        value = Config.get_locale()
        if not value.startswith('zh'): value = value.split('_')[0]
        try:
            self.pkgs = package_dict[value]
        except KeyError:
            self.pkgs = package_dict['en']
    def support(self):
        return get_arch() == 32

class Realplayer32:
    'RealPlayer® 11'
    detail = _('If you cannot play RMVB video, try this application!\n'
       'Official site: <span color="blue"><u>http://www.real.com/linux</u></span>\n'
       'You can launch RealPlayer by "/opt/real/RealPlayer/realplay".')
    category = 'media'
    logo = 'realplayer.png'
    def install(self):
        f = R(
['http://software-dl.real.com/079f1e1c74ca25924402/unix/RealPlayer11GOLD.rpm'],
8655672, 'b67f5b0b8c1103c4ed584442e44ccc724a6fbfa7').download()
        RPM.install_local(f)
    def installed(self):
        return RPM.installed('RealPlayer')
    def remove(self):
        RPM.remove('RealPlayer')

class GoogleChrome:
    __doc__ = _('Google Chrome browser')
    detail = _(
        'This is the web browser from Google. \n'
        'You can change themes by opening web-page https://tools.google.com/chrome/intl/pt/themes/index.html in Google Chrome.')
    category = 'internet'
    def install(self):
        if get_arch() == 32:
            f = R('http://dl.google.com/linux/direct/google-chrome-beta_current_i386.rpm').download()
        else:
            f = R('http://dl.google.com/linux/direct/google-chrome-beta_current_x86_64.rpm').download()
        RPM.install_local(f)
    def installed(self):
        return RPM.installed('google-chrome-beta')
    def remove(self):
        return RPM.remove('google-chrome-beta')
    def get_reason(self, f):
        if RPM.installed('google-chrome-unstable'):
            print >>f, _('"google-chrome-beta" is not installed. '
                         'However, you have installed "google-chrome-unstable".'),

class VirtualBox(_rpm_install):
    'SUN® VirtualBox 3'
    detail = _('It is the only professional virtual machine which is freely available '
       'under the terms of GPL. '
       'Official site: http://www.virtualbox.org/wiki/Downloads')
    category = 'vm'
    manual = True
    logo = 'virtualbox.png'
    depends = Repo_VirtualBox
    pkgs = 'virtualbox'

class Skype(_rpm_install):
    'Skype'
    detail = _('With Skype you can make free calls over the Internet to other people. ')
    category = 'internet'
    depends = Repo_Skype
    pkgs = 'skype'
    def support(self):
        return get_arch() == 32

class VirtualBox_OSE(_rpm_install):
    __doc__ = _('VirtualBox open source edition')
    detail = _('Command: yum install VirtualBox-OSE')
    category = 'vm'
    license = 'GNU General Public License (GPL)'
    logo = 'virtualbox.png'
    depends = Repo_RPMFusion_Free
    pkgs = 'VirtualBox-OSE'

class Repo_Chromium(_repo):
    'Chromium'
    detail = _('Open source web browser')
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
