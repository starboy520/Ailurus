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

if UBUNTU or MINT or FEDORA:
    from apps_eclipse import *

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
        if get_arch() == 32:
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
            if get_arch() == 32:
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

class CreateDesktopFolder(I):
    __doc__ = _('Create a directory "Desktop" in your home folder')
    detail = _('Create a directory "Desktop" which is linked to the desktop. After that, you can chdir to the desktop folder by command "cd ~/Desktop".')
    def __init__(self):
        import os
        self.desktop = os.path.expanduser('~/Desktop')
    def install(self):
        import os
        if not os.path.exists(self.desktop):
            # read file
            with open( os.path.expanduser('~/.config/user-dirs.dirs') ) as f:
                contents = f.readlines()
            # get name
            name = None
            for line in contents:
                if line.strip()[0] == '#': continue
                if 'XDG_DESKTOP_DIR' in line:
                    name = line.strip().split('=')[1]
                    if name[0] == '"' and name[-1] == '"': name = name[1:-1]
                    name = os.path.expandvars(name)
            # create link
            if name and os.path.exists(name):
                run('ln -s %s %s'%(name,self.desktop))
    def installed(self):
        import os 
        return os.path.exists(self.desktop)
    def remove(self):
        import os
        if os.path.islink(self.desktop):
            run('rm -f '+self.desktop)
  
class Electric(_path_lists):
    __doc__ = _('Electric: A software for IC design which supports VHDL and Verilog')
    detail = ( _('Official site: <span color="blue"><u>http://www.staticfreesoft.com/</u></span>') +
               _(' This application depends on Java.') )
    category = 'em'
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

class Speed_Up_Firefox(I):
    __doc__ = _('Speed up Firefox')
    detail = _('Firefox is faster when Pango rendering is disabled. '
        'The trick is to launch Firefox by the command: "export MOZ_DISABLE_PANGO=1; firefox". '
        'Ailurus will create a new icon "Firefox without Pango (faster)" in the menu "Applications"-->"Internet".')
    def install(self):
        paths = [
                 '/usr/share/applications/firefox-3.5.desktop',
                 '/usr/share/applications/firefox.desktop', 
                 '/usr/share/applications/mozilla-firefox.desktop',
                 '/usr/share/applications/abrowser.desktop',
                 ]
        for path in paths:
            import os
            if os.path.exists(path): break
        else:
            raise Exception('Firefox shortcut is not found.')
            
        with open(path) as f:
            content = f.readlines()
        for i, line in enumerate(content):
            if line.startswith('Exec='):
                firefox_launcher = line.split('=')[1].strip()
                new = 'Exec=sh -c "export MOZ_DISABLE_PANGO=1; %s"\n'%firefox_launcher
                content[i] = new
            if line.startswith('Name='):
                content[i] = 'Name=%s\n'%_('Firefox without Pango (faster)')
        dir = '/usr/local/share/applications/'
        if not os.path.exists(dir): run_as_root('mkdir ' + dir)
        with TempOwn(dir + 'firefox.nopango.desktop') as o:
            with open(dir + 'firefox.nopango.desktop', 'w') as f:
                f.writelines(content)

    def installed(self):
        import os 
        return ( os.path.exists('/usr/local/share/applications/firefox.nopango.desktop') or
                 os.path.exists('/usr/share/applications/firefox.nopango.desktop') )
    def remove(self):
        run_as_root('rm -f /usr/local/share/applications/firefox.nopango.desktop')
        run_as_root('rm -f /usr/share/applications/firefox.nopango.desktop')

# I think it is better to create a page in "System setting" pane.
#class Firefox_config_tweak(I):
#    __doc__ = _('Some Useful Firefox Tweak')
#    detail = (_('There are some useful tweaks can help you make Firefox easy to use.\n'
#                'All tweaks comes from DaringSoule (daringsoule@bluevalley.net), Thanks a lot!'))
#    def install(self):
#	run('cp /' + self.firefox_path + '/prefs.js ' + '/' + self.firefox_path + '/prefs.js.bak')
#	run('cp /usr/share/ailurus/support/user.js ' + '/'+self.firefox_path)
#
#    def installed(self):
#        return (os.path.isfile('/' +self.firefox_path + '/user.js'))
#    def remove(self):
#        run('rm /' + self.firefox_path + '/user.js')
#        run('cp /' + self.firefox_path + '/prefs.js.bak ' + '/' + self.firefox_path + '/prefs.js')
#    def __init__(self):
#        self.firefox_path = FirefoxExtensions.get_extensions_path()[1:-11] 

class OpenJUMP(_path_lists):
    __doc__ = _('OpenJUMP: A geographic information system')
    detail = ( 
              _('Official site: http://openjump.org/ .') +
              _(' This application depends on Java.') )
    license = GPL
    category = 'geography'
    license = GPL
    def __init__(self):
        self.shortcut = '/usr/share/applications/openjump.desktop'
        self.dir = '/opt/openjump-1.3'
        self.paths = [self.shortcut, self.dir]
    def install(self):
        f = R(
['http://ncu.dl.sourceforge.net/project/jump-pilot/OpenJUMP/1.3/openjump-v1.3.zip'],
12431980, '4df9363f0e41c797f99265107d57184b8c394ae8').download()

        with Chdir('/tmp') as o:
            run('unzip -oq %s'%f)
            import os
            if not os.path.exists('/opt'):
                run_as_root('mkdir /opt')
            if not os.path.exists(self.dir):
                run_as_root('mv openjump-1.3 /opt/')
            create_file(self.shortcut, '''[Desktop Entry]
Name=OpenJUMP
Exec=bash /opt/openjump-1.3/bin/openjump.sh
Encoding=UTF-8
StartupNotify=true
Terminal=false
Type=Application
Categories=Science;Engineering; ''')

class QueryBeforeRmALotFiles(I) :
    __doc__ = _('Query you before delete more than three files')
    detail = _('If you try to delete more than three files by "rm *", '
       'BASH will ask you a question "remove all argument?" to make sure if you really want to delete files. '
       'This is useful if you mistype "rm subdir/*" as "rm subdir/ *".\n'
       'The trick behind is to add this line into "$HOME/.bashrc".\n'
       'alias rm="rm -I"')
    def __init__(self):
        self.line = r"alias rm='rm -I'"
        import os
        self.bashrc = os.path.expandvars('$HOME/.bashrc')
    def install(self):
        file_append ( self.bashrc, self.line )
    def installed(self):
        return file_contain ( self.bashrc, self.line )
    def remove(self):
        file_remove ( self.bashrc, self.line )

class TeXLive2009(I):
    __doc__ = _('TeXLive 2009')
    detail = _('TeXLive is obtained from http://www.tug.org/texlive/')
    category = 'latex'
    license = ('all the material in TeX Live may be freely used, copied, '
               'modified, and redistributed, subject to the sources remaining freely available. '
               'See http://www.tug.org/texlive/copying.html')
    def install(self):
        import os
        #prepare xzdec
        if get_arch() == 32:
            xzdec = R(['http://www.tug.org/texlive/xz/xzdec.i386-linux'],
               69556, '974f3ddeae66d34c5e5de3c7cd9651f249e677e7').download()
        else:
            xzdec = R(['http://www.tug.org/texlive/xz/xzdec.x86_64-linux'],
               73856, '0272dce41fdf2d3da1eeda6574238a1ed18e05d6').download()
        import os, stat
        os.chmod(xzdec, stat.S_IRWXU)
        #download iso.xz
        isoxz = R([
'http://ftp.ctex.org/mirrors/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.comp.hkbu.edu.hk/pub/TeX/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.jaist.ac.jp/pub/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.fu-berlin.de/tex/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://ftp.chg.ru/pub/TeX/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',
'ftp://carroll.aset.psu.edu/pub/CTAN/systems/texlive/Images/texlive2009-20091107.iso.xz',],
1481859808,
).download()
        #extract
        print _('Unpacking ... Please wait for a few minutes.')
        #do not use 'run' or 'gksudo'
        print '%s %s > /tmp/texlive.iso'%(xzdec, isoxz)
        assert os.system('%s %s > /tmp/texlive.iso'%(xzdec, isoxz) ) == 0
        #mount
        if not os.path.exists('/mnt/texlive'):
            run_as_root("mkdir /mnt/texlive")
        run_as_root("mount -o iocharset=utf8,loop /tmp/texlive.iso /mnt/texlive")
        #launch install-tl
        import tempfile
        temp = tempfile.NamedTemporaryFile(mode='w')
        temp.write("I\n") # Do not establish symbolic links in /usr/bin/ since TeXLive 
        temp.flush()
        
        run_as_root_in_terminal('/mnt/texlive/install-tl < %s\n' % temp.name)
        run_as_root("umount /mnt/texlive")
        run_as_root("rmdir /mnt/texlive", ignore_error=True)
        #setup environment variables
        env = ETCEnvironment()
        if get_arch()==32:
            binpath = "/usr/local/texlive/2009/bin/i386-linux"
        else:
            binpath = "/usr/local/texlive/2009/bin/x86_64-linux" 
        env.add('PATH', binpath)
        env.add('MANPATH', '/usr/local/texlive/2009/texmf/doc/man')
        env.add('INFOPATH', '/usr/local/texlive/2009/texmf/doc/info')
        env.save()
        notify(_('TeXLive is installed.'), _('TeXLive will not work until you restart the computer.'))
    def installed(self):
        import os
        return os.path.exists('/usr/local/texlive/2009/')
    def remove(self):
        run_as_root('rm -rf /usr/local/texlive/2009/')
        #remove environment variables
        env = ETCEnvironment()
        if get_arch()==32:
            binpath = "/usr/local/texlive/2009/bin/i386-linux"
        else:
            binpath = "/usr/local/texlive/2009/bin/x86_64-linux" 
        env.remove('PATH', binpath)
        env.remove('MANPATH', '/usr/local/texlive/2009/texmf/doc/man')
        env.remove('INFOPATH', '/usr/local/texlive/2009/texmf/doc/info')
        env.save()
        
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
        self.range = '3.0.9~3.7'
        self.name = u'Adblock Plus'
        self.R = R(['http://ftp.mozilla.org/pub/mozilla.org/addons/1865/adblock_plus-1.1.1-fx+sm+tb.xpi'],
    297455, 'e95e558d65759a078935c61b4f937f1dcb31527d')
        _ff_extension.__init__(self)

class FFAutoProxy(_ff_extension):
    __doc__ = _('AutoProxy: Proxy management via a third party list')
    Chinese = True
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/zh-CN/firefox/addon/11009'
        self.range = '3.0.9~3.7'
        self.name = u'AutoProxy'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/11009/autoproxy-0.3b4.0+.2009110800-fx+sm+tb.xpi'],
    108858, '03f7b46e5a042491dffc08022360cb4ba7efc9d1')
        _ff_extension.__init__(self)

class FFChromeTheme_3_0(_ff_extension):
    __doc__ = _('Chrome Theme for Firefox 3.0.*')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    def __init__(self):
        self.desc = _('A coat of Chrome for Firefox 3.0.*')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/8782'
        self.range = '3.0.*'
        self.name = u'Chromifox'
        self.R = R(['https://addons.mozilla.org/en-US/firefox/downloads/file/37478/chromifox-1.0-fx.jar'],
    1290316, '7ee2366a8efad2e94936871eed7a7e93feb0c238')
        _ff_extension.__init__(self)

class FFChromeTheme_3_5(_ff_extension): 
    __doc__ = _('Chrome Theme for Firefox 3.5.*')
    license = TRI_LICENSE(MPL, GPL, LGPL)
    def __init__(self):
        self.desc = _('A coat of Chrome for Firefox 3.5.*')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/8782'
        self.range = '3.5.*'
        self.name = u'Chromifox Basic'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/8782/chromifox_basic-1.1.3-fx.jar'],
    1358662, '88e277d849021d8ee91dcbf40ccc8ecd8fe1138c')
        _ff_extension.__init__(self)

class FFCleanHide(_ff_extension):
    __doc__ = _('CleanHide: Delete hidden text in web page')
    license = GPL
    def __init__(self):
        self.desc = _('If you find that some web page use hidden text and you cannot copy text easily, try this!')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3648'
        self.range = '1.5~3.5'
        self.name = u'CleanHide'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/3648/cleanhide-1.1.0-fx+mz.xpi'],
    22341, '25812c05a1a2d944151654f9982974853c052b1e')
        _ff_extension.__init__(self)

class FFDownloadStatusBar(_ff_extension): 
    __doc__ = _('DownloadStatusBar: Keep track of downloads in a tiny statusbar.')
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/26'
        self.range = '3.0~3.7'
        self.name = u'Download Statusbar'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/26/download_statusbar-0.9.6.5-fx.xpi'],
    455756, '4d47871f71877853c6194bf559f699db33f36ee1')
        _ff_extension.__init__(self)

class FFDownThemAll(_ff_extension):
    __doc__ = _('DownThemAll: A reliable multithread downloader')
    license = GPL
    def __init__(self):
        self.desc = _('It is able to download all images on web-pages.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/201'
        self.range = '3.0~3.6'
        self.name = u'DownThemAll!'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/201/downthemall!-1.1.7-fx+tb+sm.xpi'],
    543251, 'e8ec30863e5e42de87128ce269a2af2a60bcb4b1')
        _ff_extension.__init__(self)

class FFEasyDragToGo(_ff_extension):
    __doc__ = _('EasyDragToGo: Open new tabs by dragging text, links and pictures')
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/6639'
        self.range = '2.0~3.6'
        self.name = u'Easy DragToGo'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/6639/easy_dragtogo-1.1.2.4-fx.xpi'],
    31537, '580bc24dc0b1ecd4dbddb001db0a7cad829d2f63')
        _ff_extension.__init__(self)

class FFFireBug(_ff_extension):
    __doc__ = _('FireBug: Real-time edit and debug CSS/HTML/JavaScript in webpage')
    category = 'firefoxdev'
    license = BSD
    def __init__(self):
        self.desc = _('This is a powerful web development tool.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/1843'
        self.range = '3.0~3.6'
        self.name = u'Firebug'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/1843/firebug-1.4.5-fx.xpi'],
                     695194,'aded0b0b673aec35bf5e56861e2aa8edf75d0375')
        _ff_extension.__init__(self)

class FFFireGesture(_ff_extension):
    __doc__ = _('FireGesture: Execute commands and user scripts by mouse gestures')
    license = MPL
    def __init__(self):
        self.desc = _('It supports five kinds of mouse gestures.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/6366'
        self.range = '3.0~3.7'
        self.name = u'FireGestures'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/6366/firegestures-1.5.5.1-fx.xpi'],
    70977, 'fce7abe465349cc34f36e8750fe7ad5b3441a8e9')
        _ff_extension.__init__(self)

class FFFlashgot(_ff_extension):
    __doc__ = _('Flashgot: A lightweight and reliable download managers')
    license = GPL
    def __init__(self):
        self.desc = _("It is able to download all the links, movies and audio clips of a page with a single click.")
        self.download_url = 'https://addons.mozilla.org/zh-CN/firefox/addon/220'
        self.range = '1.5~3.7'
        self.name = u'Flashgot'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/220/flashgot-1.2.1.08-fx+mz+sm+tb.xpi'],
                 324682 ,'d5660b2cde7045dce582051480a133c57e0ca75a')
        _ff_extension.__init__(self)

class FFFoxyProxy(_ff_extension):
    __doc__ = _('FoxyProxy: One-click switching proxy')
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2464'
        self.range = '3.0~3.7'
        self.name = u'FoxyProxy Standard'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/2464/foxyproxy_standard-2.15-fx+sm+tb.xpi'],
    578121, 'd839747995e9d0b1cc6b2c445b754687daed520a')
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
        self.range = '1.5~3.5.*'
        self.name = u'Greasemonkey'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/748/greasemonkey-0.8.20090920.2-fx.xpi'],
    143260, '0f1c48493e3b52a48e9b55db054a2022c46a8d08')
        _ff_extension.__init__(self)

class FFLiveHTTPHeaders(_ff_extension):
    __doc__ = _('Live HTTP Headers: View HTTP headers in real-time')
    category = 'firefoxdev'
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3829'
        self.range = '0.8~3.5.* '
        self.name = u'Live HTTP Headers'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/3829/live_http_headers-0.15-fx+sm.xpi',],
                     108354,'d6cb0b4ca29c998247f03a34d786ec61f052fb44')
        _ff_extension.__init__(self)

class FFNoscript(_ff_extension):
    __doc__ = _('NoScript: Allow active content to run only from sites you trust')
    license = GPL
    def __init__(self):
        self.desc = _(
              'Allow active content to run only from sites you trust, and protect yourself against XSS and Clickjacking attacks.' )
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/722'
        self.range = '1.5~3.7'
        self.name = u'NoScript'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/722/noscript-1.9.9.27-fx+sm+fn.xpi'],
                   457099, '7d7fa86b8a927531c5a1ff793b2a0ae39d6a8773')
        _ff_extension.__init__(self)    

class FFRadioGet(_ff_extension):
    __doc__  = _('SHA-DA network radio: Listen to and watch radio and TV programs in China')
    Chinese = True
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'http://ipget.cn/RadioGet/'
        self.range = '2.0~3.6'
        self.name = u'RadioGet'
        self.R = R(['http://ipget.cn/RadioGet/RadioGet-0.9.xpi'],
    15870, '132b45fd31dff76676d6d66bbe2b0f556f2f34fd')
        _ff_extension.__init__(self)

class FFSeoQuake(_ff_extension):
    __doc__ = _('SeoQuake: Help you view search engine parameters of your web site')
    category = 'firefoxdev'
    license = MPL
    def __init__(self):
        self.desc = _('It helps you promote your web sites.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/3036'
        self.range = '2.0~3.6.*'
        self.name = u'SeoQuake'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/3036/seoquake-2.5.9-fx.xpi',],
                     222226,'b52c18a1607cafa70243226c8861c8d9a7591d48')
        _ff_extension.__init__(self)

class FFStylish(_ff_extension):
    __doc__ = _('Stylish: Install themes and skins for websites.')
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/2108'
        self.range = '3.0~3.7'
        self.name = u'Stylish'
        self.R = R(['http://addons.mozilla.org/en-US/firefox/downloads/latest/2108/addon-2108-latest.xpi'])
        _ff_extension.__init__(self)

class FFTamperData(_ff_extension):
    __doc__ = _('Tamper Data: View and modify HTTP/HTTPS headers and post request parameters.')
    category = 'firefoxdev'
    license = GPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/966'
        self.name = u'Tamper Data'
        self.range = '2.0~3.5.*'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/966/tamper_data-10.1.0-fx.xpi',],
                     84175,'09027a308cdc23e7c245896b331e9d6f859107d1')
        _ff_extension.__init__(self)

class FFUserAgentSwitcher(_ff_extension):
    __doc__ = _('User Agent Switcher: Camousflag Firefox as other kinds of browsers.')
    license = GPL
    def __init__(self):
        self.desc = _('It tells the remote websites that you are an IE user.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/59'
        self.range = '1.0~3.6.*'
        self.name = u'User Agent Switcher'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/59/user_agent_switcher-0.7.2-fx+sm.xpi',],
                      38477,'fa4c7dcf9751e3239b14c2c441bb85e83450c678')
        _ff_extension.__init__(self)

class FFViewSourceChart(_ff_extension):
    __doc__ = _('View Source Chart: Show pretty color-coded HTML source code')
    category = 'firefoxdev'
    license = GPL
    def __init__(self):
        self.desc = _("This extension helps you quickly scan and recognize a document's tags.")
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/655'
        self.range = '1.0~3.6.*'
        self.name = u'View Source Chart'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/655/view_source_chart-2.7-fx.xpi',],
                      29360,'6b7e07b806e2a8158cad85413bb50d28e4680755')
        _ff_extension.__init__(self)

class FFWeaveSync35(_ff_extension):
    __doc__ = _('Weave Sync: synchronize bookmarks, browsing history and tabs wherever you go.')
    license = MPL
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/10868'
        self.range = '3.5~3.7'
        self.name = u'Weave'
        self.R = R(['http://ftp.mozilla.org/pub/mozilla.org/addons/10868/weave-1.0b3-fx+fn+sm.xpi'],
    360287, '23c23f795f564272348276f48cb506c7feabdad0')
        _ff_extension.__init__(self)

class FFWebDeveloper(_ff_extension):
    __doc__ = _('Web Developer: Web page analysis tools')
    category = 'firefoxdev'
    license = LGPL
    def __init__(self):
        self.desc = _('Many developers installed it.')
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/60'
        self.range = '1.0~3.6.*'
        self.name = u'Web Developer'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/60/web_developer-1.1.8-fx+sm.xpi',],
                        408412,'acd5e3e05a903f3e4c899a53a5db32cf2977ce1a')
        _ff_extension.__init__(self)

class FFYetAnotherSmoothScrolling(_ff_extension):
    __doc__ = _('Yet Another Smooth Scrolling: Customize scrolling behavior')
    license = BSD
    def __init__(self):
        self.desc = ''
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/5846'
        self.range = '1.5~3.6.*'
        self.name = u'Yet Another Smooth Scrolling'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/5846/yet_another_smooth_scrolling-2.0.25-fx.xpi'],
                    31014, '6fdcb60292a4103d7e83f79a5ccd5b480d341a3f')
        _ff_extension.__init__(self)

class FFYSlow(_ff_extension):
    __doc__ = _("YSlow: web page performance tuning")
    category = 'firefoxdev'
    license = MPL
    def __init__(self):
        self.desc = _("It helps you improve web page performance. It tells you why web page is slow.")
        self.download_url = 'https://addons.mozilla.org/en-US/firefox/addon/5369'
        self.range = '2.0~3.5.*'
        self.name = u'YSlow'
        self.R = R(['http://releases.mozilla.org/pub/mozilla.org/addons/5369/yslow-2.0.2-fx.xpi',],
                     215568,'6b90f75c4064b32ca21d720d7b6e40ecf8c024b7')
        _ff_extension.__init__(self)


