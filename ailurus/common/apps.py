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

class Generic_Genome_Browser(I):
    __doc__ = _('Generic Genome Browser')
    detail = _('Generic Genome Browser is a combination of database and interactive web page '
               'for manipulating and displaying annotations on genomes.\n'
               '<span color="red">Due to the limitation of the authors\' programming ability, '
               '"Generic Genome Browser" cannot be detected or removed by Ailurus.</span>')
    license = AL
    category='biology'
    def install(self):
        if FEDORA:
            for package in ['perl-libwww-perl', 'perl-CPAN']:
                if not RPM.installed(package): RPM.install(package)
        
        f = R('http://gmod.svn.sourceforge.net/viewvc/gmod/Generic-Genome-Browser/trunk/bin/gbrowse_netinstall.pl').download()
        run_as_root_in_terminal('perl ' + f)
    def installed(self):
        return False
    def remove(self):
        raise NotImplementedError

class Bioclipse(_path_lists):
    __doc__ = _('Bioclipse: an awesome Chemical and Biological Informatics application')
    detail = _('It is from http://sourceforge.net/projects/bioclipse/files/bioclipse2/')
    category = 'biology'
    license = ('Eclipse Public License (EPL) + exception, '
               'see http://www.bioclipse.net/license-0')
    def __init__(self):
        self.shortcut = '/usr/share/applications/bioclipse.desktop'
        self.path = '/opt/bioclipse'
        self.paths = [ self.shortcut, self.path ]
    def install(self):
        if is32():
            f = R(['http://sourceforge.net/projects/bioclipse/files/bioclipse2/bioclipse2.0/bioclipse2.0.linux.gtk.x86.zip/download'],
                  filename = 'bioclipse2.0.linux.gtk.x86.zip').download()
        else:
            f = R(['http://sourceforge.net/projects/bioclipse/files/bioclipse2/bioclipse2.0/bioclipse2.0.linux.gtk.x86_64.zip/download'],
                  filename = 'bioclipse2.0.linux.gtk.x86_64.zip').download()
        with Chdir('/tmp') as o:
            run('unzip -qo %s' %f)
            import os
            if not os.path.exists('/opt'): run_as_root('mkdir /opt')
            run_as_root('rm /opt/bioclipse -rf')
            if is32():
                run_as_root('mv bioclipse2.0.linux.gtk.x86/bioclipse /opt/')
            else:
                run_as_root('mv bioclipse2.0.linux.gtk.x86_64/bioclipse /opt/')
            run_as_root('chown $USER:$USER /opt/bioclipse -R')
            
            create_file(self.shortcut,'''[Desktop Entry]
Name=Bioclipse
Exec=/opt/bioclipse/bioclipse
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Development
Icon=/opt/bioclipse/icon.xpm 
''')
            
            file_append('/opt/bioclipse/bioclipse.ini', '-Dorg.eclipse.swt.browser.XULRunnerPath=/usr/lib/xulrunner/')

class Electric(_path_lists):
    __doc__ = _('Electric: A software for IC design which supports VHDL and Verilog')
    detail = ( _('Official site: <span color="blue"><u>http://www.staticfreesoft.com/</u></span>') +
               _(' This application depends on Java.') )
    category = 'electronics'
    license = GPL
    def __init__(self):
        self.shortcut = '/usr/share/applications/electric.desktop'
        self.file = '/opt/electricBinary.jar'
        self.paths = [self.shortcut, self.file]
    def install(self):
        f = R(
['http://ftp.gnu.org/pub/gnu/electric/electricBinary-8.09.jar'],
11102701, 'c50557bc54b74948e707dc4606009bd93274ec71').download()

        run_as_root('mkdir /opt', ignore_error=True)
        run_as_root('cp %s %s'%(f, self.file) )
        create_file(self.shortcut, '''[Desktop Entry]
Name=Electric
Exec=java -jar %s -Xms512M -Xmx1024M -Dsun.java2d.opengl=true
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering;'''%self.file)

class SweetHome3D(_path_lists):
    __doc__ = _('SweetHome3D: open source interior design application')
    detail = _('Official site:') + ' http://www.sweethome3d.com/'
    category = 'design'
    shortcut = '/usr/share/applications/SweetHome3D.desktop'
    path = '/opt/SweetHome3D-2.3'
    paths = [shortcut, path]
    def install(self):
        if is32(): url = 'http://ncu.dl.sourceforge.net/project/sweethome3d/SweetHome3D/SweetHome3D-2.3/SweetHome3D-2.3-linux-x86.tgz'
        else:       url = 'http://ncu.dl.sourceforge.net/project/sweethome3d/SweetHome3D/SweetHome3D-2.3/SweetHome3D-2.3-linux-x64.tgz'
        f = R([url]).download()
        run_as_root('mkdir /opt', ignore_error=True)
        with Chdir('/opt') as c:
            run_as_root('tar xf ' + f)
        create_file(self.shortcut, '[Desktop Entry]\n'
                                   'Name=SweetHome3D\n'
                                   'Exec=' + self.path + '/SweetHome3D\n'
                                   'Encoding=UTF-8\n'
                                   'StartupNotify=true\n'
                                   'Terminal=false\n'
                                   'Type=Application\n'
                                   'Categories=Graphics;\n')

# Do not install it via Launchpad, because the packages there is 1.6. It is old, since 1.8 has been released. 
class Songbird(I):
    __doc__ = _('Songbird: Open source substitution of iTunes')
    detail = (_('Music player which integrates with online content via plugins. '
               'Site contains project news, download, add-ons directory, help, and how to contribute.') + '\n' + 
              _('Please download from:') + ' http://developer.songbirdnest.com/builds/trunk/latest/\n' + 
              _('Launch it by this command:') + ' LD_BIND_NOW=1 ./songbird')
    
    category = 'player'
    license = GPL
    def install(self):
        open_web_page('http://developer.songbirdnest.com/builds/trunk/latest/')
    def installed(self):
        return False
    def remove(self):
        pass

#class OpenJUMP(_path_lists):
#    __doc__ = _('OpenJUMP: A geographic information system')
#    detail = ( 
#              _('Official site: http://openjump.org/ .') +
#              _(' This application depends on Java.') )
#    license = GPL
#    category = 'geography'
#    def __init__(self):
#        self.shortcut = '/usr/share/applications/openjump.desktop'
#        self.dir = '/opt/openjump-1.3'
#        self.paths = [self.shortcut, self.dir]
#    def install(self):
#        f = R(
#['http://ncu.dl.sourceforge.net/project/jump-pilot/OpenJUMP/1.3/openjump-v1.3.zip'],
#12431980, '4df9363f0e41c797f99265107d57184b8c394ae8').download()
#
#        with Chdir('/tmp') as o:
#            run('unzip -oq %s'%f)
#            import os
#            if not os.path.exists('/opt'):
#                run_as_root('mkdir /opt')
#            if not os.path.exists(self.dir):
#                run_as_root('mv openjump-1.3 /opt/')
#            create_file(self.shortcut, '''[Desktop Entry]
#Name=OpenJUMP
#Exec=bash /opt/openjump-1.3/bin/openjump.sh
#Encoding=UTF-8
#StartupNotify=true
#Terminal=false
#Type=Application
#Categories=Science;Engineering; ''')

class TsingHuaTeXTemplate(_download_one_file):
    __doc__ = _('LaTeX Thesis Templates by Tsing Hua University, China')
    import os
    detail = _('These templates include undergraduate dissertation template, master thesis template and PhD thesis template. '
       'They are developed by Tsing Hua University, China. Official website is http://thuthesis.sourceforge.net/\n'
       'After installation, a file "thuthesis.tgz" is placed in the folder "%s".')%os.environ['HOME']
    category = 'latex'
    Chinese = True
    license = 'GPL'
    def __init__(self):
        self.R = R(
['http://thuthesis.googlecode.com/files/thuthesis-4.5.1.tgz'],
9101319, '7f617b66479cafe7c01b7b104e0392a947a064ef')
        import os
        self.file = os.path.expandvars('$HOME/thuthesis.tgz')

class FFAdblock(_ff_extension):
    __doc__ = _('Adblock+: Block 99% advertisement')
    license = MPL
    def __init__(self):
        self.desc = _('It is able to block 99% ads and banners.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/1865'
        self.name = u'Adblock Plus'
        self.R = R(latest(1865), filename='adblock_plus.xpi')
        _ff_extension.__init__(self)

class FFAutoProxy(_ff_extension):
    __doc__ = _('AutoProxy: Proxy management via a third party list')
    Chinese = True
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/zh-CN/firefox/addon/11009'
        self.name = u'AutoProxy'
        self.R = R(latest(11009), filename='autoproxy.xpi')
        _ff_extension.__init__(self)

class FFChromifox(_ff_extension): 
    __doc__ = _('Chromifox: Chrome theme')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    def __init__(self):
        self.desc = _('A coat of Chrome for Firefox')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/8782'
        self.name = u'Chromifox Basic'
        self.R = R(latest(8782), filename='chromifox_basic.jar')
        _ff_extension.__init__(self)

class FFCleanHide(_ff_extension):
    __doc__ = _('CleanHide: Delete hidden text in web page')
    license = GPL
    def __init__(self):
        self.desc = _('If you find that some web page use hidden text and you cannot copy text easily, try this!')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3648'
        self.name = u'CleanHide'
        self.R = R(latest(3648), filename='cleanhide.xpi')
        _ff_extension.__init__(self)

class FFDownloadStatusBar(_ff_extension): 
    __doc__ = _('DownloadStatusBar: Keep track of downloads in a tiny statusbar.')
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/26'
        self.name = u'Download Statusbar'
        self.R = R(latest(26), filename='download_statusbar.xpi')
        _ff_extension.__init__(self)

class FFDownThemAll(_ff_extension):
    __doc__ = _('DownThemAll: A reliable multithread downloader')
    license = GPL
    def __init__(self):
        self.desc = _('It is able to download all images on web-pages.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/201'
        self.name = u'DownThemAll!'
        self.R = R(latest(201), filename='downthemall.xpi')
        _ff_extension.__init__(self)

class FFEasyDragToGo(_ff_extension):
    __doc__ = _('EasyDragToGo: Open new tabs by dragging text, links and pictures')
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/6639'
        self.name = u'Easy DragToGo'
        self.R = R(latest(6639), filename='easy_dragtogo.xpi')
        _ff_extension.__init__(self)

class FFFireBug(_ff_extension):
    __doc__ = _('FireBug: Real-time edit and debug CSS/HTML/JavaScript in webpage')
    category = 'firefox_extension'
    license = BSD
    def __init__(self):
        self.desc = _('This is a powerful web development tool.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/1843'
        self.name = u'Firebug'
        self.R = R(latest(1843), filename='firebug.xpi')
        _ff_extension.__init__(self)

class FFFireGesture(_ff_extension):
    __doc__ = _('FireGesture: Execute commands and user scripts by mouse gestures')
    license = MPL
    def __init__(self):
        self.desc = _('It supports five kinds of mouse gestures.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/6366'
        self.name = u'FireGestures'
        self.R = R(latest(6366), filename='firegestures.xpi')
        _ff_extension.__init__(self)

class FFFlashgot(_ff_extension):
    __doc__ = _('Flashgot: A lightweight and reliable download managers')
    license = GPL
    def __init__(self):
        self.desc = _("It is able to download all the links, movies and audio clips of a page with a single click.")
        self.download_url = 'https://addons.mozilla.org/zh-CN/firefox/addon/220'
        self.name = u'Flashgot'
        self.R = R(latest(220), filename='flashgot.xpi')
        _ff_extension.__init__(self)

class FFFoxyProxy(_ff_extension):
    __doc__ = _('FoxyProxy: One-click switching proxy')
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2464'
        self.name = u'FoxyProxy Standard'
        self.R = R(latest(2464), filename='foxyproxy_standard.xpi')
        _ff_extension.__init__(self)

class FFGreaseMonkey(_ff_extension):
    __doc__ = _('GreaseMonkey: Make change to web pages')
    license = MIT
    def __init__(self):
        self.desc = _('This is an extension that allow you to install scripts to make changes to web page, such as adding an HTML signature and bypassing image verification.'
              'You can download hundreds of scripts from http://userscripts.org, or '
              'check out http://wiki.greasespot.net/ to get started to write your own scripts. '
              'The book "Dive into Greasemonkey" is worth reading. It can be downloaded freely from http://diveintogreasemonkey.org/ .' )
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/748'
        self.name = u'Greasemonkey'
        self.R = R(latest(748), filename='greasemonke.xpi')
        _ff_extension.__init__(self)

class FFLiveHTTPHeaders(_ff_extension):
    __doc__ = _('Live HTTP Headers: View HTTP headers in real-time')
    category = 'firefox_extension'
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3829'
        self.name = u'Live HTTP Headers'
        self.R = R(latest(3829), filename='live_http_headers.xpi')
        _ff_extension.__init__(self)

class FFNoscript(_ff_extension):
    __doc__ = _('NoScript: Allow active content to run only from sites you trust')
    license = GPL
    def __init__(self):
        self.desc = _(
              'Allow active content to run only from sites you trust, and protect yourself against XSS and Clickjacking attacks.' )
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/722'
        self.name = u'NoScript'
        self.R = R(latest(722), filename='noscript.xpi')
        _ff_extension.__init__(self)    

class FFRadioGet(_ff_extension):
    __doc__  = _('SHA-DA network radio: Listen to and watch radio and TV programs in China')
    Chinese = True
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'http://ipget.cn/RadioGet/'
        self.name = u'RadioGet'
        # We add a second url because ipget.cn is in expiration date now :(
        self.R = R(['http://ipget.cn/RadioGet/RadioGet-0.9.xpi', 'http://ailurus.googlecode.com/files/RadioGet-0.9.xpi'],
    15870, '132b45fd31dff76676d6d66bbe2b0f556f2f34fd')
        _ff_extension.__init__(self)

class FFSeoQuake(_ff_extension):
    __doc__ = _('SeoQuake: Help you view search engine parameters of your web site')
    category = 'firefox_extension'
    license = MPL
    def __init__(self):
        self.desc = _('It helps you promote your web sites.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3036'
        self.name = u'SeoQuake'
        self.R = R(latest(3036), filename='seoquake.xpi')
        _ff_extension.__init__(self)

class FFStylish(_ff_extension):
    __doc__ = _('Stylish: Install themes and skins for websites.')
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2108'
        self.name = u'Stylish'
        self.R = R(latest(2108), filename='stylish.xpi')
        _ff_extension.__init__(self)

class FFTamperData(_ff_extension):
    __doc__ = _('Tamper Data: View and modify HTTP/HTTPS headers and post request parameters.')
    category = 'firefox_extension'
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/966'
        self.name = u'Tamper Data'
        self.R = R(latest(966), filename='tamper_data.xpi')
        _ff_extension.__init__(self)

class FFUserAgentSwitcher(_ff_extension):
    __doc__ = _('User Agent Switcher: Camousflag Firefox as other kinds of browsers.')
    license = GPL
    def __init__(self):
        self.desc = _('It tells the remote websites that you are an IE user.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/59'
        self.name = u'User Agent Switcher'
        self.R = R(latest(59), filename='user_agent_switcher.xpi')
        _ff_extension.__init__(self)

class FFViewSourceChart(_ff_extension):
    __doc__ = _('View Source Chart: Show pretty color-coded HTML source code')
    category = 'firefox_extension'
    license = GPL
    def __init__(self):
        self.desc = _("This extension helps you quickly scan and recognize a document's tags.")
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/655'
        self.name = u'View Source Chart'
        self.R = R(latest(655), filename='view_source_chart.xpi')
        _ff_extension.__init__(self)

class FFFirefoxSync(_ff_extension):
    __doc__ = _('Firefox Sync: synchronize bookmarks, browsing history and tabs wherever you go.')
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/10868'
        self.name = u'Weave'
        self.R = R(latest(10868), filename='firefox_sync.xpi')
        _ff_extension.__init__(self)

class FFWebDeveloper(_ff_extension):
    __doc__ = _('Web Developer: Web page analysis tools')
    category = 'firefox_extension'
    license = LGPL
    def __init__(self):
        self.desc = _('Many developers installed it.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/60'
        self.name = u'Web Developer'
        self.R = R(latest(60), filename='web_developer.xpi')
        _ff_extension.__init__(self)

class FFYetAnotherSmoothScrolling(_ff_extension):
    __doc__ = _('Yet Another Smooth Scrolling: Customize scrolling behavior')
    license = BSD
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/5846'
        self.name = u'Yet Another Smooth Scrolling'
        self.R = R(latest(5846), filename='yet_another_smooth_scrolling.xpi')
        _ff_extension.__init__(self)

class FFYSlow(_ff_extension):
    __doc__ = _("YSlow: web page performance tuning")
    category = 'firefox_extension'
    license = MPL
    def __init__(self):
        self.desc = _("It helps you improve web page performance. It tells you why web page is slow.")
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/5369'
        self.name = u'YSlow'
        self.R = R(latest(5369), 'yslow.xpi')
        _ff_extension.__init__(self)
