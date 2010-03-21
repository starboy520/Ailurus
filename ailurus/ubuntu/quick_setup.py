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

import sys, os
from lib import *
from libu import *
from serverlib import *
import gtk

class WelcomeDialog(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self, _('Quick setup'), None, gtk.DIALOG_NO_SEPARATOR, 
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_DELETE_EVENT, 
                                        gtk.STOCK_OK, gtk.RESPONSE_OK) )
        image = gtk.Image()
        image.set_from_file(D+'suyun_icons/default.png')
        label = gtk.Label( _('Ailurus will help you\n' 
                             '* Choose the fastest repository\n'
                             '* Install :\n'
                             '   - full language support\n'
                             '   - input method\n'
                             '   - multi-media codec\n'
                             '   - Adobe Flash support\n'
                             '   - decompression software') )
        box = gtk.HBox(False, 15)
        box.pack_start(image, False)
        box.pack_start(label, False)
        
        self.set_border_width(5)
        self.vbox.pack_start(box)
        self.vbox.show_all()

def show_check_network_splash():
    window = gtk.Window(gtk.WINDOW_POPUP)
    window.set_position(gtk.WIN_POS_CENTER)
    window.set_border_width(15)
    color = gtk.gdk.color_parse('#202020')
    window.modify_bg(gtk.STATE_NORMAL, color)
    text = gtk.Label()
    text.set_markup('<span color="yellow">%s</span>' % 
                               _('Checking whether your computer is connected to Internet ...') )
    window.add(text)
    window.show_all()
    while gtk.events_pending(): gtk.main_iteration()
    return window

def show_scan_installed_package_splash():
    window = gtk.Window(gtk.WINDOW_POPUP)
    window.set_position(gtk.WIN_POS_CENTER)
    window.set_border_width(15)
    color = gtk.gdk.color_parse('#202020')
    window.modify_bg(gtk.STATE_NORMAL, color)
    text = gtk.Label()
    text.set_markup('<span color="yellow"><big><b>%s</b></big>\n%s</span>' % 
                               ( _('Scanning installed packages.'), _('Please wait a few seconds.') ) )
    window.add(text)
    window.show_all()
    while gtk.events_pending(): gtk.main_iteration()
    return window

class WaitNetworkDialog(gtk.Dialog):
    def __continuously_ping(self):
        while not self.skip_checking:
            try:
                get_response_time('http://example.com')
                break
            except:
                import time
                time.sleep(3)
        self.destroy()

    def __skip(self):
        self.skip_checking = True

    def __init__(self):
        import thread
        thread.start_new_thread(self.__continuously_ping, () )
        
        self.skip_checking = False
        
        gtk.Dialog.__init__(self,  _('Computer is not connected to Internet'), None, gtk.DIALOG_NO_SEPARATOR,
                                      (gtk.STOCK_QUIT, gtk.RESPONSE_DELETE_EVENT) )
        
        label = gtk.Label( _('Your computer is not connected to Internet.\n'
                                         'Please configure network connections.') )
        
        edit_network_connection = image_stock_button( gtk.STOCK_CONNECT, _('Configure network connections') )
        edit_network_connection.connect('clicked', 
                                                               lambda w: KillWhenExit.add('/usr/bin/nm-connection-editor') )
        
        skip_network_checking = image_stock_button( gtk.STOCK_CANCEL, _('Skip this step'))
        skip_network_checking.connect('clicked', lambda w: self.__skip())
        
        self.set_border_width(5)
        self.vbox.pack_start(label, False, False, 10)
        self.vbox.show_all()
        self.action_area.pack_end(edit_network_connection, False)
        self.action_area.pack_end(skip_network_checking, False)
        self.action_area.show_all()

class FastestRepositoryDialog(gtk.Dialog):
    def _before_delete_event(self, *w):
        if self.can_exit == False:
            return True
        return False
    def __init__(self):
        self.can_exit = False
        gtk.Dialog.__init__(self, _('Searching the fastest repository'), None, 
                                       gtk.DIALOG_NO_SEPARATOR, None )
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('delete-event', self._before_delete_event)
        self.progress_label = gtk.Label()
        self.progress_bar = gtk.ProgressBar()
        self.timeleft_label = gtk.Label()
        self.button_start = gtk.Button('Start')
        self.button_start.connect('clicked', self.start)
        self.vbox.set_spacing(10)
        self.set_border_width(10)
        self.vbox.pack_start(self.progress_label, False)
        self.vbox.pack_start(self.progress_bar, False)
        self.vbox.pack_start(self.timeleft_label, False)
        self.show_all()
    def refresh_GUI(self):
        pass
    def start(self, *w):
        import time
        begintime = time.time()
        def show_result():
            currenttime = time.time()
            len_result = len(result)
            if len_result: server, value = result[-1]

            if len_result ==0: return
            
            #display progress
            total = len(candidate_repos)
            progress = float(len_result) / total
            self.progress_bar.set_fraction(progress)
            self.progress_bar.set_text('%s / %s' % (len_result, total) )
            #display text
            if isinstance(value, float):
                text = _("<span color='black'>Response time of %(server)s is %(value).0f ms.</span>") % {'server' : server, 'value' : value}
            elif value == 'cannot ping' or value == 'unreachable':
                text = _("<span color='black'>Server %s is unreachable.</span>") % server
            self.progress_label.set_markup(text)
            #display time left
            if len_result >= 40:
                timeleft = float(total-len_result) * (currenttime-begintime) / (len_result)
                text = _("<span color='black'>Time left: %s</span>") % derive_time(int(timeleft))
            else:
                text = _("<span color='black'>Time left: %s</span>") % _("unknown")
            if len_result % 5 == 0:
                self.timeleft_label.set_markup(text)
            
            self.refresh_GUI()

        import threading
        lock = threading.Lock()
        result = []
        threads = []
        candidate_repos = get_candidate_repositories()
        servers = [ e[3] for e in candidate_repos ]
        urls = [ e[2] for e in candidate_repos ]
        #PING servers
        for url,server in zip(urls,servers):
            while len([t for t in threads if t.isAlive()])>10: 
                import time
                time.sleep(0.1)
                show_result()
            thread = PingThread(url, server, result)
            threads.append( thread )
            thread.start()
        for thread in threads:
            if not thread.isAlive(): continue
            thread.join()
            show_result()

        #decide fastest server
        min_time = 1e8
        fastest_server = None
        for (server, time) in result:
            if not isinstance(time, float): continue
            if time<min_time:
                min_time = time
                fastest_server = server

        try:
            if not fastest_server: return
            self.progress_label.set_text( _('In order to use the fastest repository, Ailurus will change /etc/apt/sources.list') )
            self.progress_bar.set_text( _('The fastest repository is %s.')%fastest_server )
            
            for e in candidate_repos:
                if e[3] == fastest_server:
                    new_url = e[2]
                    break
            Config.set_fastest_repository(new_url)
            Config.set_fastest_repository_response_time(int(min_time))
            #check whether repositories should be changed
            for repos in get_current_official_repositories():
                assert ':' in repos
                if repos != new_url: break
            else:
                return
            self.change_server(new_url)
        except:
            import traceback
            traceback.print_exc()
        finally:
            #destroy dialog
            self.can_exit = True
            self.destroy()

    def change_server(self, fastest_url):
        #apply the fastest repository
        changes = {}
        for repos in get_current_official_repositories():
            changes[repos] = fastest_url
        notify( _('Apply the fastest repository:'), fastest_url )
        change_repositories_in_source_files(changes)
        #apt-get update
        self.progress_label.set_text( _('Run command: "sudo apt-get update"') )
        notify(_('Run "apt-get update". Please wait for few minutes.'), ' ')
        APT.apt_get_update()

class Search_Fastest_Repository:
    def installed(self):
        return False
    def install(self):
        dialog = FastestRepositoryDialog()
        dialog.button_start.emit('clicked')

class Install_Hardware_Driver:
    def installed(self):
        return False
    def install(self):
        gksudo('/usr/bin/jockey-gtk')

def get_class_by_name(name, app_classes):
    assert isinstance(name, str)
    assert isinstance(app_classes, list)
    
    import types
    for c in app_classes:
        assert isinstance(c, types.ClassType)
        if c.__name__ == name:
            return c
    g = globals()
    if name in g: 
        c = g[name]
        assert isinstance(c, types.ClassType)
        assert hasattr(c, 'install') and hasattr(c, 'installed')
        return c
    raise Exception(name)

class DoStuffDialog(gtk.Dialog):
    def get_stuff(self):
        ret =  [
            ( _('Search fastest repository'), 'Search_Fastest_Repository' ),
            ( _('Install hardware drivers'), 'Install_Hardware_Driver' ),
            ( _('Full language support and input method'), 'Full_Language_Pack' ),
            ( _('Multi-media codec'), 'Multimedia_Codecs' ),
            ( _('Decompression software: 7z, rar, cab, ace'), 
              'Decompression_Capability' ),
            ]
        if Config.is_Chinese_locale():
            ret.append( ( _('Alipay ( Zhi Fu Bao ) security plugin for Firefox'), 'AliPayFirefoxPlugin', ) )
            ret.append( ( _('Stardict and four dictionaries'), 'StardictAndDictionaries', ) )
        ret += [
            ( _(u'Adobe® Flash plugin for web browser'), 'Flash_Player' ),
            ( _('Fix font bug in Flash plugin'), 'Flash_Player_Font_Bug' ), 
            ]
        return ret
    def func_pixbuf(self, column, cell, model, iter):
        value = model.get_value(iter, 0)
        assert 0 <= value <= 3
        pixbuf = [ self.pixbuf_fail, self.pixbuf_blank, self.pixbuf_started, self.pixbuf_done ] [ value ]
        cell.set_property('pixbuf', pixbuf)
    def refresh_GUI(self):
        pass
    def start(self, *w):
        import os, sys, traceback
        try:
            run.terminal = self.terminal
            r,w = os.pipe()
            os.dup2(w, sys.stdout.fileno())
            import thread
            thread.start_new_thread(self.terminal.read, (r,) )
            
            for row in self.task_store:
                row[0] = 2
                self.refresh_GUI()
                print '\x1b[1;33m', _('Ongoing:'), row[1], '\x1b[m'
                try:
                    c = row[2]()
                    if not c.installed(): c.install()
                    row[0] = 3
                    print '\x1b[1;32m', _('Successful'), '\x1b[m'
                except:
                    row[0] = 0
                    print '\x1b[1;31m', _('Failed'), '\x1b[m'
                    traceback.print_exc()
                print
        finally:
            self.can_exit = True
            sys.stdout.flush()
            os.close(r)
            os.close(w)
            run.terminal = None
            os.dup2(self.backup_stdout, sys.stdout.fileno())

    def refresh_GUI_thread(self):
        while self.can_exit == False:
            if not gtk: break
            while gtk.events_pending(): gtk.main_iteration()
            import time
            time.sleep(0.1)

    def _before_delete_event(self, *w):
        if self.can_exit == False: return True
        return False

    def __init__(self, app_classes):
        self.can_exit = False
        
        import os, sys
        self.backup_stdout = os.dup(sys.stdout.fileno())

        gtk.Dialog.__init__(self, _('Quick setup'), None, gtk.DIALOG_NO_SEPARATOR, None )
        self.connect('delete-event', self._before_delete_event)
        
        self.start_button = gtk.Button()
        self.start_button.connect('clicked', self.start)
        
        import gobject
        # status (0=fail, 1=blank, 2=started, 3=done), text, app_class
        self.task_store = task_store = gtk.ListStore(int, str, gobject.TYPE_PYOBJECT) 
        for text, name in self.get_stuff():
            try:
                c = get_class_by_name(name, app_classes)
                task_store.append([1, text, c])
            except:
                import traceback
                traceback.print_exc()

        self.pixbuf_fail = gtk.gdk.pixbuf_new_from_file_at_size(D+'other_icons/fail.png', 16, 16)
        self.pixbuf_blank = gtk.gdk.pixbuf_new_from_file_at_size(D+'other_icons/blank.png', 16, 16)
        self.pixbuf_started = gtk.gdk.pixbuf_new_from_file_at_size(D+'other_icons/started.png', 16, 16)
        self.pixbuf_done = gtk.gdk.pixbuf_new_from_file_at_size(D+'other_icons/done.png', 16, 16)

        render_pixbuf = gtk.CellRendererPixbuf()
        render_text = gtk.CellRendererText()
        task_column = gtk.TreeViewColumn()
        task_column.pack_start(render_pixbuf)
        task_column.set_cell_data_func(render_pixbuf, self.func_pixbuf) 
        task_column.pack_start(render_text)
        task_column.add_attribute(render_text, 'text', 1)
        
        task_treeview = gtk.TreeView(task_store)
        task_treeview.append_column(task_column)
        task_treeview.set_headers_visible(False)
        task_treeview.set_rules_hint(True)
        
        task_scroll = gtk.ScrolledWindow()
        task_scroll.set_shadow_type(gtk.SHADOW_IN)
        task_scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        task_scroll.add(task_treeview)
        
        from support.terminal_single_thread import Terminal
        self.terminal = terminal = Terminal()
        
        paned = gtk.HPaned()
        paned.pack1(task_scroll, False, True)
        paned.pack2(terminal.get_widget(), True, False)
        paned.set_size_request(900, 500)
        
        self.set_border_width(5)
        self.vbox.pack_start(paned)
        self.show_all()
        
        self.button_close = gtk.Button(stock = gtk.STOCK_CLOSE)
        self.button_close.connect('clicked', lambda *w: self.destroy())
        self.action_area.pack_start(self.button_close) 

def quick_setup():
    #show welcome dialog
    dialog = WelcomeDialog()
    ret = dialog.run()
    dialog.destroy()
    assert ret != gtk.RESPONSE_DELETE_EVENT
    #check network connections
    window = show_check_network_splash()
    try:
        try:     get_response_time('http://example.com')
        finally: window.destroy()
    except:
        dialog = WaitNetworkDialog()
        ret = dialog.run()
        dialog.destroy()
        assert ret != gtk.RESPONSE_DELETE_EVENT
    #load app_classes
    window = show_scan_installed_package_splash()
    import common as COMMON
    DESKTOP = None
    import ubuntu as DISTRIBUTION
    from loader import load_app_classes
    app_classes = load_app_classes(COMMON, DESKTOP, DISTRIBUTION)
    window.destroy()
    #3
    dialog = DoStuffDialog(app_classes)
    import thread
    thread.start_new_thread(dialog.refresh_GUI_thread, () )
    dialog.start_button.emit('clicked')
    #4
    notify( _('All works are done.'), ' ' )
    dialog.action_area.show_all()
    dialog.run()

if __name__ == '__main__':
    gtk.window_set_default_icon_from_file(D+'suyun_icons/default.png')
    import os
    gtk.gdk.threads_init()
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    quick_setup()
