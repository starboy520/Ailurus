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

from lib import *
from libu import *

def url_button(url):
    import gtk
    def func(w, url): open_web_page(url)
    def enter(w, e): 
        try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        except AttributeError: pass
    def leave(w, e): 
        try: w.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.LEFT_PTR))
        except AttributeError: pass
    label = gtk.Label()
    label.set_markup("<span color='blue'><u>%s</u></span>"%url)
    button = gtk.Button()
    button.connect('clicked', func, url)
    button.connect('enter-notify-event', enter)
    button.connect('leave-notify-event', leave)
    button.set_relief(gtk.RELIEF_NONE)
    button.add(label)
    align = gtk.Alignment(0, 0.5)
    align.add(button)
    return align

def check_update():
    try:
        OLD_RELEASE_DATE = AILURUS_RELEASE_DATE 
        import gtk
        import urllib2
        import re
        if FEDORA:
            filename_pattern = r'ailurus-[0-9.]+-1\.noarch\.rpm'
            version_pattern = r'ailurus-([0-9.]+)-1\.noarch\.rpm'
            code_url = 'http://homerxing.fedorapeople.org/'
        elif UBUNTU or MINT:
            version_string = VERSION
            filename_pattern = r'ailurus_[0-9.]+-0%s1_all\.deb' % version_string
            version_pattern = r'ailurus_([0-9.]+)-0%s1_all\.deb' % version_string
            code_url = 'http://ppa.launchpad.net/ailurus/ppa/ubuntu/pool/main/a/ailurus/'
        else:
            return
        lastest_version = AILURUS_VERSION
        lastest_filename = ''
        f = urllib2.urlopen(code_url)
        for line in f.readlines():
            filenames = re.findall(filename_pattern, line)
            for filename in filenames:
                match = re.search(version_pattern, filename)
                version = match.group(1)
                if version.split('.') > lastest_version.split('.'):
                    lastest_version = version
                    lastest_filename = filename
        f.close()
        import gtk
        dlg = gtk.Dialog('',
                         None, gtk.DIALOG_NO_SEPARATOR,
                         (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))
        vbox = gtk.VBox(False, 5)
        if lastest_filename:
            dlg.set_title(_('A new version is available'))
            label = gtk.Label( _('Version %s is released.\n'
                                 'You can download it from:')
                                 % lastest_version)
            button = url_button(code_url+lastest_filename)
            vbox.pack_start(label)
            vbox.pack_start(button, False)
        else:
            dlg.set_title(_('Check update'))
            label = gtk.Label( _('You have already installed the latest Ailurus version. :)') )
            vbox.pack_start(label)
        image = gtk.Image()
        image.set_from_file(D+'suyun_icons/update.png')
        hbox = gtk.HBox(False, 5)
        hbox.pack_start(image, False)
        hbox.pack_start(vbox, False)
        dlg.vbox.pack_start(hbox, False)
        dlg.vbox.show_all()
        dlg.run()
        dlg.destroy()
    except:
        import traceback
        traceback.print_exc()

def show_about_dialog():
    import gtk
    gtk.about_dialog_set_url_hook( lambda dialog, link: 1 )
    about = gtk.AboutDialog()
    about.set_logo(gtk.gdk.pixbuf_new_from_file(D+'suyun_icons/logo.png'))
    about.set_name('Ailurus')
    about.set_version(AILURUS_VERSION)
    about.set_website_label( _('Project homepage') )
    about.set_website('http://ailurus.googlecode.com/')
    about.set_authors( [
          _('Developers:'),
          'Homer Xing <homer.xing@gmail.com>', 
          'CHEN Yangyang <skabyy@gmail.com>',
          'MA Yue <velly.empire@gmail.com>',
          'QI Chengjie <starboy.qi@gmail.com>',
          '',
          _('Contributors:'),
          'HUANG Wei <wei.kukey@gmail.com>',
          'HAN Haofu <gtxx3600@gmail.com>',
          'SHANG Yuanchun <idealities@gmail.com>',
          'DU Yue <elyes.du@gmail.com>',
           ] )
    about.set_translator_credits(_('translator-credits'))
    about.set_artists( [
          'SU Yun',
          'M. Umut Pulat    http://12m3.deviantart.com/', 
          'Andrea Soragna   http://sora-meliae.deviantart.com/',
          'Paul Davey       http://mattahan.deviantart.com/',] )
    about.set_copyright( _(u"Copyright © 2007-2010,\nTrusted Digital Technology Laboratory,\nShanghai Jiao Tong University, China.") + '\n'
                         + _(u"Copyright © 2009-2010, Ailurus Developers Team") )
    about.set_wrap_license(False)
    about.set_license(
'''
Ailurus is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

The source code in Ailurus is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ailurus; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Unlike otherwise indicated, artwork is available under the Creative Commons 
Attribution Share-alike license v3.0 or any later version. To view a copy of 
this license, visit http://creativecommons.org/licenses/by-sa/3.0/ or send 
a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco,
California, 94105, USA.

Some Rights Reserved:

The rights in the trademarks, logos, service marks of Canonical Ltd, as well as
the look and feel of Ubuntu, are subject to the Canonical Trademark Policy at
http://www.ubuntu.com/ubuntu/TrademarkPolicy 

All images in directory "data/suyun_icons" are released under the GPL License, 
version 2 or higher version. Their copyright are holded by SU Yun.

All images in directory "data/sona_icons" are released under the GPL License. 
Their copyright are holded by Andrea Soragna.

All images in directory "data/velly_icons" are released under the GPL License. 
Their copyright are holded by MA Yue.

All images in directory "data/umut_icons" and "data/appicons" are are released
under the GNU Lesser General Public License. Their copyright are holded by M. Umut Pulat.

In directory "data/other_icons":
acire.png is copied from Acire project. It is released under the GPL license.
ailurus.png is released under the GPL license. Its copyright is holded by SU Yun.
ailurus_for_splash.png is released under the GPL license. Its copyright is holded by MA Yue.
audacity.png is copied from Audacity project. It is released under the GPL license. Its copyright is holded by Audacity Team.
blank.png is released under the GPL license. Its copyright is holded by Homer Xing.
bluefish.png is copied from Bluefish project. It is released under the GPL license. Its copyright is holded by Olivier Sessink.
bluetooth.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
childsplay.png is copied from Childsplay project. It is released under the GPL license. Its copyright is holded by Stas Zytkiewicz.
codeblocks.png is copied from Code::Blocks project. It is released under the GPL v3.0 license. Its copyright is holded by Code::Blocks Team.
done.png, fail.png, parcellite.png, s_desktop.png, started.png, toolbar_back.png, toolbar_disable.png, toolbar_enable.png, toolbar_forward.png, toolbar_quit.png are copied from GNOME project. They are released under the GPL license. There copyright are holded by GNOME community.
extcalc.png is copied from Extcalc project. It is released under the GPL v2 license. Its copyright is holded by Extcalc Team.
fedora.png is copied from Fedora project. It is released under the GPL v3.0 license. Its copyright is holded by Fedora community.
firestarter.png is copied from Firestarter project. It is released under the GPL license. Its copyright is holded by Tomas Junnonen.
gcompris.png is copied from GCompris project. It is released under the GPL license. Its copyright is holded by Bruno Coudoin.
liferea.png is copied from Liferea project. It is released under the GPL license. Its copyright is holded by Liferea Team.
locale.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
stardict.png is copied from Stardict project. It is released under GPL v3 license. Its copyright is holded by Stardict Team.
m_clean_up.png is released under the GPL license. Its copyright is holded by MA Yue.
netbeans.png is copied from Netbeans project. It is released under the GPL v2 license. Its copyright is holded by Sun Microsystems Ltd.
pitivi.png is copied from PiTiVi project. It is released under the LGPL license. Its copyright is holded by PiTiVi Team.
python.png is copied from Python project. It is released under the Python license. Its copyright is holded by Python Software Foundation.
qtcreator.png is copied from Qt project. It is released under the LGPL license. Its copyright is holded by Nokia Corporation.
s_nautilus.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
songbird.png is copied from Songbird project. It is released under the GPL v2. Its copyright is holded by Songbird Team.
toolbar_study.png is released under the LGPL license. Its copyright is holded by Umut Pulat.
tux.png is released under the LGPL license. Its copyright is holded by Umut Pulat.
tuxpaint.png is copied from Tux Paint project. It is released under the GPL license. Its copyright is holded by Tux Paint Team.
ubuntu.png is copied from Ubuntu project. Its copyright is holded by Canonical Ltd. Some rights reserved: The rights in the trademarks, logos, service marks of Canonical Ltd, as well as the look and feel of Ubuntu, are subject to the Canonical Trademark Policy at http://www.ubuntu.com/ubuntu/TrademarkPolicy 
vuze.png is copied from Vuze project. It is released under the GPL license. Its copyright is holded by Vuze Team.
wallpaper-tray.png is copied from Wallpaper Tray project. It is released under the GPL license. Its copyright is holded by Wallpaper Tray Team.
worldofpadman.png is copied from World of Padman project. It is realeased under the GPL license.
xbmc.png is copied from XBMC project. It is released under the GPL license. Its copyright is holded by XBMC Team.
All rights of other images which are not mensioned above are preserves by their authors.

All rights of the applications installed by Ailurus are preserved by their authors.''')
    about.vbox.pack_start( gtk.Label( _('\nThis version is released at %s.') % AILURUS_RELEASE_DATE), False)
    about.vbox.show_all()
    about.run()
    about.destroy()

def show_special_thank_dialog():
    import StringIO
    text = StringIO.StringIO()
    print >>text, _('We wish to express thankfulness to these projects:')
    print >>text, '<b><big>Lazybuntu, UbuntuAssistant'
    print >>text, 'GTweakUI, Easy Life, Ubuntu-tweak, CPU-G</big></b>'
    print >>text
    print >>text, _('We sincerely thank these people:')
    print >>text
    print >>text, _('The people who provide inspiration:')
    print >>text, '<b><big>PCMan, Careone, novia, '
    print >>text, 'BAI Qingjie, Aron Xu, Federico Vera, '
    print >>text, 'ZHU Jiandy, Maksim Lagoshin, '
    print >>text, 'Romeo-Adrian Cioaba, David Morre, '
    print >>text, 'Liang Suilong, Lovenemesis, Chen Lei, '
    print >>text, 'DaringSoule, Ramesh Mandaleeka, JCOM</big></b>'
    print >>text
    print >>text, _('The people who designs the logo:')
    print >>text, '<b><big>SU Yun</big></b>'
    print >>text
    print >>text, _('The people who maintain PPA repository:')
    print >>text, '<b><big>Aron Xu</big></b>'
    print >>text
    print >>text, _('The people who provide a lot of Linux skills:')
    print >>text, '<b><big>Oneleaf</big></b>'
    print >>text
    print >>text, _('The people who provide a lot of Debian packages:')
    print >>text, '<b><big>Careone</big></b>'
    print >>text
    print >>text, _('The people who provide a lot of translation:')
    print >>text, '<b><big>Federico Vera, Sergey Sedov, Sérgio Marques</big></b>', 
    print >>text, _('and many other people.')
    print >>text 
    print >>text, _('The people who report bugs:')
    print >>text, '<b><big>LIU Liang, YU Pengfei, q1ha0,'
    print >>text, 'novia, hardtzh, fegue</big></b>', _('and many other people.')
    print >>text
    print >>text, _('The people who eliminate bugs:')
    print >>text, '<b><big>anjiannian, PES6, eemil.lagerspetz</big></b>'
    print >>text
    print >>text, _('The people who publicize this software:')
    print >>text, '<b><big>dsj, BingZhiGuFeng, chinairaq, coloos,'
    print >>text, 'TombDigger, sudo, Jandy Zhu</big></b>', _('and many other people.')
    print >>text
    print >>text, _('and the people not mensioned here.')
    import gtk
    label = gtk.Label()
    label.set_markup(text.getvalue())
    text.close()
    label.set_justify(gtk.JUSTIFY_CENTER)
    scroll = gtk.ScrolledWindow()
    scroll.add_with_viewport(label)
    scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    scroll.set_shadow_type(gtk.SHADOW_NONE)
    scroll.set_size_request(-1, 500)
    dialog = gtk.Dialog( _('Thanks'), None, 
        gtk.DIALOG_MODAL | 
        gtk.DIALOG_NO_SEPARATOR, 
        buttons = (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
    dialog.set_border_width(10)
    dialog.vbox.pack_start(scroll, False, False)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()

def show_changelog():
    with open(D+'/../ChangeLog') as f:
        show_text_window(_('Ailurus changelog'), f.read())
        
def show_text_window(title, content):
    import gtk
    buffer = gtk.TextBuffer()
    buffer.set_text(content)
    textview = gtk.TextView()
    textview.set_buffer(buffer)
    textview.set_editable(False)
    textview.set_cursor_visible(False)
    textview.set_wrap_mode(gtk.WRAP_WORD)
    scroll = gtk.ScrolledWindow()
    scroll.add(textview)
    scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    scroll.set_shadow_type(gtk.SHADOW_IN)
    close_button = gtk.Button(stock=gtk.STOCK_CLOSE)
    close_button.connect('clicked', lambda *w: window.destroy())
    align = gtk.Alignment(1, 0.5)
    align.add(close_button)
    vbox = gtk.VBox(False, 10)
    vbox.pack_start(scroll)
    vbox.pack_start(align, False)

    window = gtk.Window()
    window.set_title(title)
    window.add(vbox)
    window.set_default_size(600, 400)
    window.set_border_width(10)
    window.set_position(gtk.WIN_POS_CENTER)
    window.show_all()
