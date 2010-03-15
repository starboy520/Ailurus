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

class Alice(_path_lists):
    __doc__ = _('Alice: A new way to learn programming')
    detail = (
              _('A storytelling application, especially appropriate for middle school students.') +'\n' + 
              _('Official site: <span color="blue"><u>http://www.alice.org/</u></span> .') + 
              _(' This application depends on Java.') )
    category = 'education'
    size = 374600000
    time = 353
    logo = 'alice.png'
    def __init__(self):
        self.dir = '/opt/Alice 2.2'
        self.shortcut = '/usr/share/applications/alice.desktop'
        self.paths = [ self.dir, self.shortcut ]
    def install(self):
        if get_arch()==32:
            f = R(
['http://tdt.sjtu.edu.cn/S/Alice2.2b_i386.tar.bz2',],
296544228, '0c6340a5b52d72abc12c394561d61c3ccba21ca7').download()
        else:
            f = R(
['http://tdt.sjtu.edu.cn/S/Alice2.2b_x86_64.tar.bz2',],
296519582, '7558fa7f22d13f8d18671b3efc44374541c5a506').download()

        import os
        if not os.path.exists('/opt'):
            gksudo('mkdir /opt')
        own_by_user('/opt')
        FileServer.chdir('/opt')
        try:
            run('tar jxf '+f)
            assert os.path.exists(self.dir)
            create_file(self.shortcut, '''[Desktop Entry]
Name=Alice
Exec=bash "/opt/Alice 2.2/Required/alice.sh"
Path=/opt/Alice 2.2/Required/
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Education;Science; ''')
        finally:
            FileServer.chdir_back()

class AliPayFirefoxPlugin:
    __doc__ = _('Alipay ( Zhi Fu Bao ) security plugin for Firefox')
    detail = _("Official site: <span color='blue'><u>http://blog.alipay.com/301.html</u></span>")
    category = 'firefox'
    size = 240000
    Chinese = True
    logo = 'alipay.png'
    def __init__(self):
        import os
        self.path = os.path.expanduser('~/.mozilla/plugins')
    def install(self):
#        open_web_page('http://blog.alipay.com/301.html')
        file = '/tmp/aliedit.tar.gz'
        run('wget --timeout=60 http://blog.alipay.com/wp-content/2008/10/aliedit.tar.gz -O /tmp/aliedit.tar.gz')
        path = self.path
        import os
        if not os.path.exists(path):
            run('mkdir -p %s'%path)
        FileServer.chdir(path)
        try:
            run('tar zxf %s'%file)
        finally:
            FileServer.chdir_back()
    def installed(self):
        import os
        return (
          (os.path.exists(self.path+'/aliedit.so') and os.path.exists(self.path+'/aliedit.xpt'))
             or
          (os.path.exists('/usr/lib/firefox-addons/plugins/aliedit.so')
             and os.path.exists('/usr/lib/firefox-addons/plugins/aliedit.xpt'))
          )
    def remove(self):
        run('rm -f %s'%(self.path+'/aliedit.so') )
        run('rm -f %s'%(self.path+'/aliedit.xpt') )
        if os.path.exists('/usr/lib/firefox-addons/plugins/aliedit.so'):
            gksudo('rm -f /usr/lib/firefox-addons/plugins/aliedit.so')
        if os.path.exists('/usr/lib/firefox-addons/plugins/aliedit.xpt'):
            gksudo('rm -f /usr/lib/firefox-addons/plugins/aliedit.xpt')
    def support(self):
        import os
        return os.path.exists('/usr/bin/firefox')

class AstroMenace(_path_lists):
    'AstroMenace'
    detail = _('Drive a spaceship and battle against invaders! Collect money during the combat. Upgrade armaments and weapons. '
       'This is a full 3d style space shooter game. '
       'It supports mouse, keyboard and joystick control. '
       'Official site: http://www.viewizard.com/')
    size = 62265282
    time = 12
    category = 'game'
    logo = 'astromenace.png'
    def __init__(self):
        self.paths = ['/opt/astromenace', '/usr/share/applications/astromenace.desktop']
    def install(self):
        f = R(
['http://tdt.sjtu.edu.cn/S/amenace12.tar.bz2',
'http://www.viewizard.com/download/amenace12.tar.bz2'],
35948638, '752d6faec7a4432f991055ab788b1e7dba004995').download()

        import os
        if not os.path.exists('/opt'): gksudo('mkdir /opt')
        gksudo('chown $USER:$USER /opt')
        FileServer.chdir('/opt')
        try:
            run('tar xf %s'%f)
            create_file('/usr/share/applications/astromenace.desktop', 
'''[Desktop Entry]
Name=AstroMenace
Exec=/opt/astromenace/game_launcher
Path=/opt/astromenace/
Icon=/opt/astromenace/astromenace_64.png
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Game;''')
        finally:
            FileServer.chdir_back()

class EIOffice:
    __doc__ = _('Evermore Integrated Office 2009 free version')
    detail = _('It is able to edit text, spreadsheets, and slides. '
       'Official site: <span color="blue"><u>http://www.evermoresw.com.cn/webch/download/downEIOPersonal.jsp</u></span>')
    category='office'
    Chinese = True
    time=112
    size=217428*1000
    manual=True
    logo = 'eio.png'
    def install(self):
        FileServer.chdir_local()
        try:
            f = R('http://218.90.147.70/EverMore/EIOPersonal/EIOffice_Personal_Lin.tar.gz').download()
            run('tar xf %s' % f)
            run('chmod a+x EIOffice_Personal_Lin/setup')
            gksudo("EIOffice_Personal_Lin/setup")
            
            msgs = ( 
                     _('Clipboard arts are to be installed.'),
                     _('Help files are to be installed.'),
                     _('Science editor images are to be installed.'),
                     _('Templates are to be installed.')
                        )
            for file, msg in zip(
               ['http://218.90.147.70/EverMore/EIOPersonal/Resource/EIOffice_Clipart.tar.gz',
                'http://218.90.147.70/EverMore/EIOPersonal/Resource/EIOffice_HelpFiles.tar.gz',
                'http://218.90.147.70/EverMore/EIOPersonal/Resource/EIOffice_ScienceEditorImages.tar.gz',
                'http://218.90.147.70/EverMore/EIOPersonal/Resource/EIOffice_Templates.tar.gz',], msgs):
                    wget(file, '/tmp/eio.tar.gz') 
                    run("tar zxf /tmp/eio.tar.gz")
                    notify( _('Installing EIOffice'), msg )
                    gksudo("./setup")
        finally:
            FileServer.chdir_back()
    def installed(self):
        import os
        return os.path.exists('/usr/bin/eio')
    def remove(self):
        import os
        if os.path.exists('/usr/bin/rmeio'):
            gksudo('/usr/bin/rmeio')

class ChineseAcademyofSciencesTeXTemplate(_download_one_file) :
    # cannot find out which license it is released under
    __doc__ = _('LaTeX Thesis Templates by Chinese Academy of Sciences')
    import os
    detail = _('After installation, a file "CASthesis.zip" is placed in the folder "%s".')%os.path.expanduser('~')
    category = 'latex'
    time = 60 #estimated
    size = 244000 #estimated
    Chinese = True
    logo = 'texlive-templates.png'
    def __init__(self):
        self.R = R(
['http://tdt.sjtu.edu.cn/S/CASthesis-v0.1j.zip',],
244765, 'dc84597ee626b7a2dcd3ee8825d2e374f6822197')
        import os
        self.file = os.path.expanduser('~/CASthesis.zip')

class XJTUTeXTemplate(_download_one_file) :
    # cannot find out which license it is released under
    __doc__ = _("LaTeX Thesis Templates by Xi\'an Jiaotong University, China")
    import os
    detail = _('After installation, a file "XJTUthesis.rar" is placed in the folder "%s".')%os.path.expanduser('~')
    category = 'latex'
    time = 60 #estimated
    size = 3010000 #estimated
    Chinese = True
    logo = 'texlive-templates.png'
    def __init__(self):
        self.R = R(
['http://tdt.sjtu.edu.cn/S/XJTUthesis.rar',],
3009431, '88ce43f6396d76fff56b597a2a35487548fdaa54')
        import os
        self.file = os.path.expanduser('~/XJTUthesis.rar')

class HITTeXTemplate(_download_one_file) :
    # cannot find out which license it is released under
    __doc__ = _('LaTeX Thesis Templates by Harbin Institute of Technology, China')
    import os
    detail = _('After installation, a file "HITthesis.rar" is placed in the folder "%s".')%os.path.expanduser('~')
    category = 'latex'
    time = 60 #estimated
    size = 2710000 #estimated
    Chinese = True
    logo = 'texlive-templates.png'
    def __init__(self):
        self.R = R(
['http://tdt.sjtu.edu.cn/S/PlutoThesis_UTF8_1.9.2.20090424.zip',
'http://plutothesis.googlecode.com/files/PlutoThesis_UTF8_1.9.2.20090424.zip'],
2710034, 'aee937bf0a09936d78f57cd45616997af7a1ef3c')
        import os
        self.file = os.path.expanduser('~/HITthesis.rar')

class Vuze(_path_lists): 
    # The core engine is released under GPL. 
    # However, parts of Vuze carry more restricted licensing terms.
    #
    # Vuze is not in 8.04 repository.
    # Vuze 3.1.1 is in 8.10/9.04 repository.
    # Latest Vuze is in 9.10 repository.
    'Vuze 4.3'
    category = 'internet'
    logo = 'vuze.png'
    detail = _('Download via bittorrent + Search videos + Play videos')
    def __init__(self):
        self.paths = ['/opt/vuze', '/usr/share/applications/azureus.desktop']
    def install(self):
        f = R('http://hwcdn01.vuze.com/files/Vuze_Installer.tar.bz2').download()
        import os
        if not os.path.exists('/opt'): gksudo('mkdir /opt')
        gksudo('chown $USER:$USER /opt -R')
        FileServer.chdir('/opt')
        try:
            run('tar xf %s' % f)
            create_file('/usr/share/applications/azureus.desktop',
'''[Desktop Entry]
Encoding=UTF-8
Categories=Java;Network;FileTransfer;P2P
Comment=peer-to-peer file distribution tool
Exec=/opt/vuze/vuze %f
GenericName=BitTorrent client
Icon=/opt/vuze/vuze.png
MimeType=application/x-bittorrent
Name=Vuze
Type=Application''')
            if get_arch() == 64:
                f = R('http://eclipse.ialto.org/eclipse/downloads/drops/R-3.4-200806172000/swt-3.4-gtk-linux-x86_64.zip').download()
                run('unzip %s -qo -d /tmp' % f)
                run('mv /tmp/swt.jar /opt/vuze/')
        finally:
            FileServer.chdir_back()
    def support(self):
        return Config.get_Ubuntu_version() in ['hardy', 'intrepid', 'jaunty']
            
class FFJavaScriptDebugger(_ff_extension): # cannot find out which license it is released under
    __doc__ = _('JavaScript Debugger: a powerful JavaScript debugger')
    category = 'firefoxdev'
    size = 907935
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/216'
        self.range = '0.9~3.7'
        self.name = u'JavaScript Debugger'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/216/javascript_debugger-0.9.87.4-fx+tb+sb+sm.xpi'],
                      217578,'3369de2b98b747c4d1c79803819b2d727b9083f6')
        _ff_extension.__init__(self)

class FFMacOSXTheme(_ff_extension): # cannot find out which license it is released under
    __doc__ = _('Mac OS X Theme')
    logo = 'ff_macosxtheme.png'
    size = 1026679
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/7172'
        self.range = '3.0.*~3.7.*'
        self.name = u'MacOSX Theme'
        self.R = R(['http://tdt.sjtu.edu.cn/S/FirefoxExt/macosx_theme-0.6.8-fx.jar',
                    'http://releases.mozilla.org/pub/mozilla.org/addons/7172/macosx_theme-0.6.8-fx.jar'],
    689344, '4b58d1c49ae123e50a76cb41bc6a1162d1bcaaf8')
        _ff_extension.__init__(self)

class FFNetVideoHunter(_ff_extension): # cannot find out which license it is released under
    __doc__ = _('NetVideoHunter: Download videoclips from video-sharing web sites')
    logo = 'ff_netvideohunter.png'
    size = 104411
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/7447'
        self.range = '2.0~3.7'
        self.name = u'NetVideoHunter'
        self.R = R(['http://tdt.sjtu.edu.cn/S/FirefoxExt/netvideohunter-0.4.3-fx.xpi',
                    'http://releases.mozilla.org/pub/mozilla.org/addons/7447/netvideohunter-0.4.3-fx.xpi'],
                    44541, '3d47e726587743758097a069358ed306df63bc3a')
        _ff_extension.__init__(self)

class FFPersonas(_ff_extension): # cannot find out which license it is released under
    __doc__ = _('Personas: One-click changing Firefox skin')
    logo = 'ff_personas.png'
    size = 383371
    def __init__(self):
        self.desc = _('Theme your browser according to your mood, hobby or season.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/10900'
        self.range = '3.0~3.6.*'
        self.name = u'Personas'
        self.R = R(['http://tdt.sjtu.edu.cn/S/FirefoxExt/personas-1.4-fx+tb.xpi',
                    'http://releases.mozilla.org/pub/mozilla.org/addons/10900/personas-1.4-fx+tb.xpi'],
    275501, 'ac6de4e93270e0650fc06a88cf5fe639e8a879fb')
        _ff_extension.__init__(self)

