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
import gtk
from lib import *
from libu import *

def show_about_dialog(*w): # called by __help
    gtk.about_dialog_set_url_hook( lambda dialog, link: 1 )
    about = gtk.AboutDialog()
    about.set_logo(gtk.gdk.pixbuf_new_from_file(D+'suyun_icons/logo.png'))
    about.set_name('Ailurus')
    from lib import AILURUS_VERSION
    about.set_version(AILURUS_VERSION)
    about.set_website_label( _('Ailurus blog')+' http://ailurus.cn/' )
    about.set_website('http://ailurus.cn/')
    about.set_authors( [
          'Homer Xing <homer.xing@gmail.com>', 
          'CHEN Yangyang <skabyy@gmail.com>',
          'Starboy Qi <starboy.qi@gmail.com>',
          'MA Yue <velly.empire@gmail.com>' ] )
    about.set_translator_credits(_('translator-credits'))
    about.set_artists( [
          'SU Yun',
          'M. Umut Pulat    http://12m3.deviantart.com/', 
          'Paul Davey    http://mattahan.deviantart.com/',
          'andrea soragna    http://sora-meliae.deviantart.com/'] )
    about.set_copyright( _(u"Copyright © 2007-2010, Trusted Digital Technology Lab., Shanghai Jiao Tong Univ., China.") )
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

All images in directory "data/sona_icons" are released under the GPL License,
 Their copyright are holded by andrea soragna.

All images in directory "data/umut_icons" and "data/appicons" are are released
under the GNU Lesser General Public License. Their copyright are holded by M. Umut Pulat.

In directory "data/other_icons":
ailurus.png is released under the GPL license. Its copyright is holded by SU Yun.
blank.png is released under the GPL license. Its copyright is holded by Homer Xing.
bluefish.png is copied from Bluefish project. It is released under the GPL license. Its copyright is holded by Olivier Sessink.
childsplay.png is copied from Childsplay project. It is released under the GPL license. Its copyright is holded by Stas Zytkiewicz.
codeblocks.png is copied from Code::Blocks project. It is released under the GPL v3.0 license. Its copyright is holded by Code::Blocks Team.
done.png, fail.png, parcellite.png, s_desktop.png, started.png, toolbar_back.png, toolbar_disable.png, toolbar_enable.png, toolbar_forward.png, toolbar_quit.png are copied from GNOME project. They are released under the GPL license. There copyright are holded by GNOME community.
extcalc.png is copied from Extcalc project. It is released under the GPL v2 license. Its copyright is holded by Extcalc Team.
fedora.png is copied from Fedora project. It is released under the GPL v3.0 license. Its copyright is holded by Fedora community.
firestarter.png is copied from Firestarter project. It is released under the GPL license. Its copyright is holded by Tomas Junnonen.
gcompris.png is copied from GCompris project. It is released under the GPL license. Its copyright is holded by Bruno Coudoin.
liferea.png is copied from Liferea project. It is released under the GPL license. Its copyright is holded by Liferea Team.
stardict.png is copied from Stardict project. It is released under GPL v3 license. Its copyright is holded by Stardict Team.
netbeans.png is copied from Netbeans project. It is released under the GPL v2 license. Its copyright is holded by Sun Microsystems Ltd.
python.png is copied from Python project. It is released under the Python license. Its copyright is holded by Python Software Foundation.
qtcreator.png is copied from Qt project. It is released under the LGPL license. Its copyright is holded by Nokia Corporation.
s_nautilus.png is copied from GNOME project. It is released under the GPL license. Its copyright is holded by GNOME community.
toolbar_study.png is released under the LGPL license. Its copyright is holded by Umut Pulat.
tux.png is released under the LGPL license. Its copyright is holded by Umut Pulat.
tuxpaint.png is copied from Tux Paint project. It is released under the GPL license. Its copyright is holded by Tux Paint Team.
ubuntu.png is copied from Ubuntu project. Its copyright is holded by Canonical Ltd. Some rights reserved: The rights in the trademarks, logos, service marks of Canonical Ltd, as well as the look and feel of Ubuntu, are subject to the Canonical Trademark Policy at http://www.ubuntu.com/ubuntu/TrademarkPolicy 
vuze.png is copied from Vuze project. It is released under the GPL license. Its copyright is holded by Vuze Team.
wallpaper-tray.png is copied from Wallpaper Tray project. It is released under the GPL license. Its copyright is holded by Wallpaper Tray Team.

All rights of other images which are not mensioned above are preserves by their authors.

All rights of the applications installed by Ailurus are preserved by their authors.''')
    about.vbox.pack_start( gtk.Label( _('Welcome to leave response in blog~') ) , False, False )
    def read_changelog_callback(*w):
        buffer = gtk.TextBuffer()
        with open('/usr/share/ailurus/ChangeLog') as f:
            buffer.set_text(f.read())
        textview = gtk.TextView()
        textview.set_buffer(buffer)
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        scroll = gtk.ScrolledWindow()
        scroll.add(textview)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        dialog = gtk.Dialog( _('Ailurus changelog'), None, 
                             gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR, 
                             buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
        dialog.set_border_width(10)
        dialog.vbox.pack_start(scroll)
        dialog.vbox.set_size_request(700, 500)
        dialog.vbox.show_all()
        dialog.run()
        dialog.destroy()

    from lib import AILURUS_RELEASE_DATE
    about.vbox.pack_start( gtk.Label( _('\nThis version is released at %s.') % AILURUS_RELEASE_DATE), False)
    about.vbox.show_all()
    read_changelog = gtk.Button(_('Read changelog'))
    read_changelog.connect('clicked', read_changelog_callback)
    about.action_area.pack_start(read_changelog, False, False )
    about.action_area.reorder_child(read_changelog, 0)
    about.action_area.show_all()
    about.run()
    about.destroy()

def show_special_thank_dialog(widget): # called by __help
    import StringIO
    text = StringIO.StringIO()
    print >>text, _('We wish to express thankfulness to these projects:')
    print >>text, '<b><big>Lazybuntu, UbuntuAssistant'
    print >>text, 'GTweakUI, Easy Life, Ubuntutweak, CPU-G</big></b>'
    print >>text
    print >>text, _('We sincerely thank these people:')
    print >>text
    print >>text, _('The people who provide inspiration:')
    print >>text, '<b><big>PCMan, Careone, novia, '
    print >>text, 'BAI Qingjie, Aron Xu, Federico Vera, '
    print >>text, 'ZHU Jiandy, Maksim Lagoshin, '
    print >>text, 'Romeo-Adrian Cioaba, David Morre</big></b>'
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
    print >>text, '<b><big>Federico Vera, Sergey Sedov</big></b>', _('and many other people.')
    print >>text 
    print >>text, _('The people who report bugs:')
    print >>text, '<b><big>LIU Liang, YU Pengfei, q1ha0,'
    print >>text, 'novia, hardtzh, fegue</big></b>', _('and many other people.')
    print >>text
    print >>text, _('The people who eliminate bugs:')
    print >>text, '<b><big>anjiannian, PES6</big></b>'
    print >>text
    print >>text, _('The people who publicize this software:')
    print >>text, '<b><big>dsj, BingZhiGuFeng, chinairaq, coloos,'
    print >>text, 'TombDigger, sudo, Jandy Zhu</big></b>', _('and many other people.')
    print >>text
    print >>text, _('and the people not mensioned here.')
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
        gtk.DIALOG_NO_SEPARATOR)
    dialog.set_border_width(10)
    dialog.vbox.pack_start(scroll, False, False)
    dialog.vbox.show_all()
    dialog.run()
    dialog.destroy()

def to_date(string): #called by check_update 
    List = string.strip().split('-')
    import datetime
    return datetime.date( int(List[0]), int(List[1]), int(List[2]) )

def check_update(*w):
    try:
        import gtk
        # hide the clicked menu item
        while gtk.events_pending(): gtk.main_iteration()
        
        from libu import url_button
        from lib import AILURUS_RELEASE_DATE as OLD_RELEASE_DATE
    
        import urllib2
        f = urllib2.urlopen('http://ailurus.googlecode.com/files/latest')
        release_date_string = f.readline().strip()
        deb_file_name = f.readline().strip()
        f.close()
        
        new_release_date = to_date(release_date_string)
        old_release_date = to_date(OLD_RELEASE_DATE)
        
        import gtk
        dlg = gtk.Dialog(_('Updates for Ailurus'),
                         None, gtk.DIALOG_NO_SEPARATOR,
                         (gtk.STOCK_CLOSE, gtk.RESPONSE_OK))
        vbox = gtk.VBox(False, 5)
        if new_release_date > old_release_date:
            label = gtk.Label( _('A new version is released at %(date)s.')
                           %{'date':release_date_string})
            button = url_button('http://ailurus.googlecode.com/files/'+deb_file_name)
            vbox.pack_start(label)
            vbox.pack_start(button, False)
        else:
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
    
def __study_linux(main_view):
    study_url_items = [ 
        # (use stock?, stock name or icon path, text, web page url, Chinese only?
#        (True, gtk.STOCK_HELP, _(u'How to use Intel® compiler & math library ?'), 
#         'http://tdt.sjtu.edu.cn/S/how_to/icc_mkl_tbb.html', False),
        (True, gtk.STOCK_HELP, _('How to compile a LaTeX file into pdf file ?'), 
         'http://ailurus.cn/?p=329', False),
         ]

    def __get_menu(items):
        ret = []
        for item in items:
            if item == None: 
                ret.append( gtk.SeparatorMenuItem() )
                continue 
            if item[4]==False or (item[4] and Config.is_Chinese_locale()):
                if item[0]: menu_item = image_stock_menuitem(item[1], item[2])
                else: menu_item = image_file_menuitem(item[2], item[1], 16, 3)
                menu_item.url = item[3]
                menu_item.connect('activate', lambda w: open_web_page(w.url))
                ret.append( menu_item )
        return ret
    
    ret = __get_menu(study_url_items)
    study_show_tip = image_file_menuitem(_('Tip of the day'), D+'sora_icons/m_tip_of_the_day.png', 16, 3)
    def show_day_tip(*w):
        from support.tipoftheday import TipOfTheDay
        w=TipOfTheDay()
        w.run()
        w.destroy()
    study_show_tip.connect('activate', show_day_tip)
    ret.insert(0, study_show_tip)
    ret.insert(1, gtk.SeparatorMenuItem() )
    return ret

def __set_wget_options(w): # called by __preferences
    current_timeout = Config.wget_get_timeout()
    current_tries = Config.wget_get_triesnum()
    
    adjustment_timeout = gtk.Adjustment(current_timeout, 1, 60, 1, 1, 0)
    scale_timeout = gtk.HScale(adjustment_timeout)
    scale_timeout.set_digits(0)
    scale_timeout.set_value_pos(gtk.POS_BOTTOM)
    timeout_label = label_left_align(_('How long after the server does not respond, give up downloading? (in seconds)'))
    
    adjustment_tries = gtk.Adjustment(current_tries, 1, 20, 1, 1, 0)
    scale_tries = gtk.HScale(adjustment_tries)
    scale_tries.set_digits(0)
    scale_tries.set_value_pos(gtk.POS_BOTTOM)
    tries_label = label_left_align(_('How many times does Ailurus try to download the same resource?'))
    
    dialog = gtk.Dialog(
        _('Set Ailurus download parameter'), 
        None, gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR, 
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK) )
    dialog.set_border_width(5)
#    dialog.set_size_request(500,-1)
    dialog.vbox.pack_start(timeout_label, False)
    dialog.vbox.pack_start(scale_timeout, False)
    dialog.vbox.pack_start(tries_label, False)
    dialog.vbox.pack_start(scale_tries, False)
    dialog.vbox.show_all()
    #display dialog
    ret = dialog.run()
    #get parameter
    new_timeout = int(adjustment_timeout.get_value())
    new_tries = int(adjustment_tries.get_value())
    dialog.destroy()
    #write back
    if ret == gtk.RESPONSE_OK:
        Config.wget_set_timeout(new_timeout)
        Config.wget_set_triesnum(new_tries)

def __preferences(main_view):
    menu_tooltip = gtk.CheckMenuItem( _("""Don't show "tip of the day" on start up""") )
    menu_tooltip.set_active( Config.get_disable_tip() )
    menu_tooltip.connect('toggled', 
            lambda w: notify(_('Preferences changed'), _('Your changes will take effect at the next time when the program starts up.')) 
                              or Config.set_disable_tip(w.get_active()) )
    
    menu_tip_after_logging_in = gtk.CheckMenuItem( _('Show a random Linux skill after you log in to GNOME') )
    menu_tip_after_logging_in.set_active(ShowALinuxSkill.installed())
    def toggled(w):
        if w.get_active(): ShowALinuxSkill.install()
        else: ShowALinuxSkill.remove()
        notify(_('Preferences changed'), _('Your changes will take effect at the next time when you log in to GNOME.') )
    menu_tip_after_logging_in.connect('toggled', toggled)
    
    menu_set_wget_option = gtk.MenuItem(_("Set download parameters"))
    menu_set_wget_option.connect('activate', __set_wget_options)
    
    return [ menu_tooltip, menu_tip_after_logging_in, menu_set_wget_option ]

def __others(main_view):
    help_blog = image_stock_menuitem(gtk.STOCK_HOME, _('Ailurus blog'))
    help_blog.connect('activate', 
        lambda w: open_web_page('http://ailurus.cn/' ) )
    
    help_update = image_file_menuitem(_('Check for updates'), D+'suyun_icons/m_check_update.png', 16, 3) 
    help_update.connect('activate', check_update)

    help_report_bug = image_file_menuitem(_('Propose suggestion and report bugs'), D+'sora_icons/m_propose_suggestion.png', 16, 3) 
    help_report_bug.connect('activate', 
        lambda w: report_bug() )
    
    help_translate = image_stock_menuitem(gtk.STOCK_CONVERT, _('Translate this application'))
    help_translate.connect('activate', 
        lambda w: open_web_page('https://translations.launchpad.net/ailurus/trunk' ) )
    
    special_thank = gtk.MenuItem( _('Special thanks') )
    special_thank.connect('activate', show_special_thank_dialog)
    
    about = gtk.MenuItem( _('About') )
    about.connect('activate', show_about_dialog)
    
    return [ help_blog, help_update, help_report_bug, help_translate, special_thank, about ] 

def get_study_linux_menu(main_view):
    return __study_linux(main_view)

def get_preferences_menu(main_view):
    return __preferences(main_view)

def get_others_menu(main_view):
    return __others(main_view)