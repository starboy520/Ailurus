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

class Multimedia_Codecs (_rpm_install) :
    __doc__ = _('Multi-media codec')
    detail = _(
       'Command: yum install '
       'gstreamer gstreamer-plugins-bad gstreamer-plugins-bad-extras gstreamer-plugins-base'
                     'gstreamer-plugins-good gstreamer-plugins-ugly')
    category = 'media'
    logo = 'codec.png'
    def __init__(self):
        self.pkgs = ('gstreamer gstreamer-plugins-bad gstreamer-plugins-bad-extras gstreamer-plugins-base'
                     'gstreamer-plugins-good gstreamer-plugins-ugly')
    def install(self):
        obj = Repo_RPMFusion_Free()
        if not obj.installed(): obj.install()
        
        _rpm_install.install(self)
    def get_reason(self, f):
        self._get_reason(f)

class Flash_Player(_rpm_install):
    __doc__ = _(u'Adobe® Flash plugin for web browser')
    detail = _('Command: yum install flash-plugin')
    category = 'media'
    logo = 'flash.png'
    def __init__(self):
        self.pkgs = 'flash-plugin'
    def install(self):
        obj = Repo_Adobe()
        if not obj.installed(): obj.install()
        _rpm_install.install(self)

class AdobeReader(_rpm_install):
    __doc__ = _(u'Adobe® PDF Reader')
    detail = _('Official site: http://get.adobe.com/cn/reader/')
    category = 'office'
    logo = 'adobereader.png'
    def __init__(self):
        package_dict = {
                   'zh_HK':'AdobeReader_cht',
                   'zh_TW':'AdobeReader_cht',
                   'zh_CN':'AdobeReader_chs',
                   'de':'AdobeReader_deu',
                   'en_US':'AdobeReader_enu',
                   'es':'AdobeReader_esp',
                   'it':'AdobeReader_ita',
                   'nl':'AdobeReader_nld',
                   'pt':'AdobeReader_ptb',
                   }
        import locale
        value = locale.getdefaultlocale()[0]
        if not value in Config.supported_locale():
            value = value.split('_')[0]
        if not value in package_dict:
            value = 'en_US'
        self.pkgs = package_dict[value]
    def install(self):
        #
        obj = Repo_Adobe()
        if not obj.installed(): 
            obj.install()
        #
        _rpm_install.install(self)
    def support(self):
        return get_arch() == 32

class FoxitReader:
    'FoxitReader'
    detail = ( _('A light weight pdf reader.') + '\n' +
               _('Official site: <span color="blue"><u>http://www.foxitsoftware.com/pdf/desklinux/</u></span>') )
    category = 'office'
    logo = 'foxitreader.png'
    def install(self):
        f = R(
['http://mirrors.foxitsoftware.com/pub/foxit/reader/desktop/linux/1.x/1.0/enu/FoxitReader-1.0-1.i386.rpm'],
3409078, 'ad7793cdf20be9beb0297c8339943f5a168b3997').download()
        RPM.install_local(f)
    def installed(self):
        return RPM.installed('FoxitReader')
    def remove(self):
        RPM.remove('FoxitReader')

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

class VirtualBox:
    'SUN® VirtualBox 3'
    detail = _('It is the only professional virtual machine which is freely available '
       'under the terms of GPL. '
       'Official site: http://www.virtualbox.org/wiki/Downloads')
    category = 'vm'
    manual = True
    logo = 'virtualbox.png'
    def install(self):
        arch = get_arch()
        version = Config.get_Fedora_version()
        if arch==32 and (version=='9' or version=='10'):
            r = R('http://download.virtualbox.org/virtualbox/3.1.2/VirtualBox-3.1-3.1.2_56127_fedora9-1.i386.rpm',
                  46609460, 'ac913c2ad3b866d6ece874d9a2fe3d014abe4525')
        elif arch==64 and (version=='9' or version=='10'):
            r = R('http://download.virtualbox.org/virtualbox/3.1.2/VirtualBox-3.1-3.1.2_56127_fedora9-1.x86_64.rpm',
                  46984379, '2ddc67ba217a07d8e553c8a176620dfe6002a3f3')
        elif arch==32 and version=='11':
            r = R('http://download.virtualbox.org/virtualbox/3.1.2/VirtualBox-3.1-3.1.2_56127_fedora11-1.i586.rpm',
                  47099692, '8eca6f4b176e19cb9769b44a47fb3b395bf6590f')
        elif arch==64 and version=='11':
            r = R('http://download.virtualbox.org/virtualbox/3.1.2/VirtualBox-3.1-3.1.2_56127_fedora11-1.x86_64.rpm',
                  47066896, '89019d7047a7f9d3e7ca0bfff838126f3d087d72')
        elif arch==32 and version=='12':
            r = R('http://download.virtualbox.org/virtualbox/3.1.2/VirtualBox-3.1-3.1.2_56127_fedora12-1.i686.rpm',
                  41230264, '676451e3fb16d2656fb2b953a4def31691b7d2b2')
        elif arch==64 and version=='12':
            r = R('http://download.virtualbox.org/virtualbox/3.1.2/VirtualBox-3.1-3.1.2_56127_fedora12-1.x86_64.rpm',
                  41402824, '2eb67cf16e09ba327e99b2954650bad9c80d4abc')
        else: raise Exception(arch, version)
        
        f = r.download()
        RPM.install_local(f)
    def installed(self):
        return RPM.installed('VirtualBox')
    def remove(self):
        RPM.remove('VirtualBox')

class Skype(_rpm_install):
    'Skype'
    detail = _('With Skype you can make free calls over the Internet to other people. ')
    category = 'internet'
    def support(self):
        return get_arch() == 32
    def __init__(self):
        self.pkgs = 'skype'
    def install(self):
        obj = Repo_Skype()
        if not obj.installed(): obj.install()
        
        _rpm_install.install(self)

class Native_64bit_Flash(_path_lists):
    __doc__ = _('Adobe native 64bit Flash plugin for Firefox')
    category = 'media'
    logo = 'flash.png'
    def __init__(self):
        self.paths = [
            '/usr/lib/mozilla/plugins/libflashplayer.so',
            '/usr/lib/firefox-addons/plugins/libflashplayer.so',
            '/usr/lib/xulrunner-addons/plugins/libflashplayer.so',
            ]
    def install(self):
        su('bash '+D+'../support/fedora-native-64bit-flash-installer.sh')
    def support(self):
        return get_arch() == 64

