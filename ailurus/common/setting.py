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
import gtk
import sys, os
from lib import *
from libu import *
from libsetting import *

def __change_kernel_swappiness():
    vbox = gtk.VBox()
    text_box = gtk.HBox(False)
    text_box.pack_start( gtk.Label( _('0 = Swap little mem to disk') ), False, False )
    text_box.pack_start( gtk.Label(), True, True, 30 )
    text_box.pack_start( gtk.Label( _('100 = Swap a lot of mem to disk') ), False, False )
    
    current_value = int( get_output('/sbin/sysctl -n vm.swappiness').strip() )
    adjustment = gtk.Adjustment(current_value, 0, 100, 10, 10, 0)
    def update(adjustment):
        new_value = round( adjustment.value, -1 )
        adjustment.set_value( new_value )
    adjustment.connect("value_changed", update)
    scale = gtk.HScale(adjustment)
    scale.set_digits(0)
    scale.set_value_pos(gtk.POS_BOTTOM)

    def apply(w, adjustment):
        new_value = int( adjustment.get_value() )
        new_line = 'vm.swappiness = %s' % new_value
        with TempOwn('/etc/sysctl.conf') as o:
            with open('/etc/sysctl.conf') as f:
                contents = f.readlines()
            for i, line in enumerate(contents):
                if line[0]=='#' or line=='\n': continue
                if 'vm.swappiness' in line:
                    contents[i] = new_line
                    break
            else:
                contents.append(new_line)
            with open('/etc/sysctl.conf', 'w') as f:
                f.writelines(contents)
        try:
            run_as_root('/sbin/sysctl -p', ignore_error = True)
            current_value = int( get_output('/sbin/sysctl -n vm.swappiness').strip() )
            if current_value != new_value: raise CommandFailError
        except AccessDeniedError:
            pass
    
    apply_button = image_stock_button(gtk.STOCK_APPLY, _('Apply') )
    apply_button.connect('clicked', apply, adjustment)
    align_apply_button = gtk.HBox(False, 0)
    align_apply_button.pack_end(apply_button, False)
    
    vbox.pack_start(text_box, False, False)
    vbox.pack_start(scale, False, False)
    vbox.pack_start(align_apply_button, False, False)
    vbox.set_size_request(500, -1)
    align_vbox = gtk.Alignment(0, 0)
    align_vbox.add(vbox)
    return Setting(align_vbox, _('Change the tendency of swapping memory to disk'), ['memory'])

def __restart_network():
     def restart_network(w):
         try:
             import dbus
             bus = dbus.SystemBus()
             obj = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager')
             obj.sleep(dbus_interface='org.freedesktop.NetworkManager')
             obj.wake(dbus_interface='org.freedesktop.NetworkManager')
             if UBUNTU or UBUNTU_DERIV:
                 notify(' ', _('Run command: ')+'/etc/init.d/networking restart')
                 try:
                     run_as_root('/etc/init.d/networking restart')
                 except AccessDeniedError:
                     pass
             notify(_('Information'), _('Network restarted successfully.'))
         except: pass
     button_restart_network = gtk.Button(_('Restart network').center(30))
     button_restart_network.connect('clicked', restart_network)
     button_restart_network.set_tooltip_text(_('These commands will be executed:\n'
               'dbus-send --system --dest=org.freedesktop.NetworkManager '
               '--type=method_call /org/freedesktop/NetworkManager '
               'org.freedesktop.NetworkManager.sleep\n'
               'dbus-send --system --dest=org.freedesktop.NetworkManager '
               '--type=method_call /org/freedesktop/NetworkManager '
               'org.freedesktop.NetworkManager.wake\n'
               'sudo /etc/init.d/networking restart'))
     align_bfm = gtk.Alignment(0, 0.5)
     align_bfm.add(button_restart_network)
     vbox = gtk.VBox()
     vbox.set_border_width(10)
     vbox.pack_start(align_bfm, False)
     return Setting(vbox, _('Restart network'), ['network'])
 
def __change_hostname(): 
#   I have to use the class, to resolve problem of these codes:
#        def __value_changed(button):
#            button.set_sensitive(True)
#
#        def __button_clicked(entry):
#            new_host_name = entry.get_text()
#            button.set_sensitive(False)
#   error message is 'free variable referenced before assignment'. I don't know the reason.
    class change_host_name(gtk.HBox):
        def __value_changed(self, *w):
            self.button.set_sensitive(True)

        def __button_clicked(self, *w):
            new_host_name = self.entry.get_text()
            with TempOwn('/etc/hosts') as o:
                with open('/etc/hosts') as f:
                    content = f.read()
                    content = content.replace(self.old_host_name, new_host_name)
                with open('/etc/hosts', 'w') as f:
                    f.write(content)
            if UBUNTU or UBUNTU_DERIV:
                with TempOwn('/etc/hostname') as o:
                    with open('/etc/hostname', 'w') as f:
                        f.write(new_host_name)
            elif FEDORA:
                with TempOwn('/etc/sysconfig/network') as o:
                    with open('/etc/sysconfig/network') as f:
                        content = f.read()
                        content = content.replace(self.old_host_name, new_host_name)
                    with open('/etc/sysconfig/network', 'w') as f:
                        f.write(content)       
            else:
                dialog = gtk.Dialog('Feature is not implemented', None, gtk.DIALOG_MODAL|gtk.DIALOG_NO_SEPARATOR,
                                     buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))
                dialog.vbox.pack_start(gtk.Label('This feature has not been implement for your Linux distribution'))
                dialog.vbox.show_all()
                dialog.run()
                dialog.destroy()      
                            
            self.button.set_sensitive(False)
        
        def __init__(self):
            self.entry = gtk.Entry()
            self.button = gtk.Button(_('Apply'))
            self.label = gtk.Label(_('New host name:'))
            self.old_host_name = get_output('hostname')
            self.entry.set_text(self.old_host_name)
            self.entry.connect('changed', self.__value_changed)
            self.button.connect('clicked', self. __button_clicked)
                
            gtk.HBox.__init__(self, False, 5)
            self.pack_start(self.label, False)
            self.pack_start(self.entry, False)
            self.pack_start(self.button, False)
            
    hbox = change_host_name()
    return Setting(hbox, _('Change host name'), ['host_name'])

def __configure_firefox():
    content_max_tokenizing_time_t = FirefoxPrefText(_('maximum number of microseconds between two page rendering'), 'content.max.tokenizing.time')
    content_max_tokenizing_time = FirefoxNumericPref('content.max.tokenizing.time', 0, 5000000, 50000, 360000)

    content_notify_backoffcount_t = FirefoxPrefText(_('re-render pages until this number has been reached'), 'content.notify.backoffcount')
    content_notify_backoffcount = FirefoxNumericPref('content.notify.backoffcount', -1, 500, 1, -1)
    
    network_dnsCacheEntries_t = FirefoxPrefText(_('the number of DNS results to cache'), 'network.dnsCacheEntries')
    network_dnsCacheEntries = FirefoxNumericPref('network.dnsCacheEntries', 0, 256, 16, 20)
    
    network_dnsCacheExpiration_t = FirefoxPrefText(_('the number of seconds to cache DNS results'), 'network.dnsCacheExpiration')
    network_dnsCacheExpiration = FirefoxNumericPref('network.dnsCacheExpiration', 60, 86400, 120, 60)
    
    network_ftp_idleConnectionTimeout_t = FirefoxPrefText(_('the number of seconds before the FTP connection times out'), 'network.ftp.idleConnectionTimeout')
    network_ftp_idleConnectionTimeout = FirefoxNumericPref('network.ftp.idleConnectionTime', 60, 300, 60, 300)
    
    network_http_keep_alive_timeout_t = FirefoxPrefText(_('amount of time in seconds to keep alive connections'), 'network.http.keep-alive.timeout', 
                                                        _('alive connections can be re-used for multiple requests, therefore improve performance.'))
    network_http_keep_alive_timeout = FirefoxNumericPref('network.http.keep-alive.timeout', 30, 300, 10, 300)
    
    network_http_max_persistent_connections_per_proxy_t = FirefoxPrefText(_('the total number of alive connections per proxy server'),
                                                                          'network.http.max-persistent-connections-per-proxy',
                                                                          'If more connections are needed, they are queued until a connection "slot" is available.')
    network_http_max_persistent_connections_per_proxy = FirefoxNumericPref('network.http.max-persistent-connections-per-proxy', 1, 255, 1, 24)
    
    nglayout_initialpaint_delay_t = FirefoxPrefText(_('The number of milliseconds to wait before first displaying the page.'),
                                                    'nglayout.initialpaint.delay', 
                                                    _("Since the start of a web page normally doesn't have much useful information to display, "
                                                      "Firefox will wait a short interval before first rendering a page."))
    nglayout_initialpaint_delay = FirefoxNumericPref('nglayout.initialpaint.delay', 0, 250, 25, 250)
    
    network_http_max_connections_t = FirefoxPrefText(_('the maximum number of HTTP connections'),
                                                     'network.http.max-connections',
                                                     _('Users on slower connections may want to reduce this number to help prevent HTTP connection timeouts. '
                                                       'Users on faster connections may want to increase it.'))
    network_http_max_connections = FirefoxNumericPref('network.http.max-connections', 1, 65535, 96, 30)
    
    network_http_max_connections_per_server_t = FirefoxPrefText(_('The maximum number of connections to a single server'), 'network.http.max-connections-per-server')
    network_http_max_connections_per_server = FirefoxNumericPref('network.http.max-connections-per-server', 1, 255, 16, 32)
    
    browser_sessionstore_max_tabs_undo_t = FirefoxPrefText(_('Increase/Decrease History Undo Close Tab Limit'), 'browser.sessionstore.max_tabs_undo')
    browser_sessionstore_max_tabs_undo = FirefoxNumericPref('browser.sessionstore.max_tabs_undo', 5, 50, 4, 10)
    
    browser_blink_allowed_t = FirefoxPrefText(_('display blink text'), 'browser.blink_allowed')
    browser_blink_allowed = FirefoxBooleanPref('browser.blink_allowed')
    
    browser_tabs_tab_min_width_t = FirefoxPrefText(_('Set the the width of narrowest tab'), 'browser.tabs.tabMinWidth',
                                                   _("To fit more tabs on the tab strip, Firefox shrinks each tab’s width. "
                                                     "This preference determines the narrowest a tab can become before the tab strip becomes scrollable "
                                                     "to handle the overflow. \n"))
    browser_tabs_tab_min_width = FirefoxNumericPref('browser.tabs.tabMinWidth', 38, 100, 1, 75)
    
    toolkit_scrollbox_scroll_increment_t = FirefoxPrefText(_('Speed of Scrolling Across Tabs'), 'toolkit.scrollbox.scrollIncrement')
    toolkit_scrollbox_scroll_increment = FirefoxNumericPref('toolkit.scrollbox.scrollIncrement', 10, 100, 5, 20)
    
    browser_urlbar_autofill_t = FirefoxPrefText(_('Auto Complete URL while You type at address Bar'), 'browser.urlbar.autoFill')
    browser_urlbar_autofill = FirefoxBooleanPref('browser.urlbar.autoFill')
    
    browser_bookmarks_auto_export_html_t = FirefoxPrefText(_('Auto export bookmarks as HTML'), 'browser.bookmarks.autoExportHTML')
    browser_bookmarks_auto_export_html = FirefoxBooleanPref('browser.bookmarks.autoExportHTML')
    
    browser_history_expire_days_t = FirefoxPrefText(_('The History expiring time'), 'browser.history_expire_days')
    browser_history_expire_days = FirefoxNumericPref('browser.history_expire_days', 1, 300, 1, 180)
    
    broswer_history_expire_sites_t = FirefoxPrefText(_('The maximum number of webpages to be recorded into the history'), 'browser.history_expire_sites')
    broswer_history_expire_sites = FirefoxNumericPref('browser.history_expire_sites', 100, 100000, 100, 40000)
    
    extension_get_addons_max_results_t = FirefoxPrefText(_('The maximum number of add-on search results'), 'extension.getAddons.maxResults')
    extension_get_addons_max_results = FirefoxNumericPref('extension.getAddons.maxResults', 1, 30, 1, 5)
    
    browser_cache_offline_capacity_t = FirefoxPrefText(_('Disk space for offline cashe'), 'browser.cache.offline.capacity',
                                                       _('set this amount to what you want to allocate'
                                                         ' the amount of disk space the offline cache may use, in kilobytes. \n'))
    browser_cache_offline_capacity = FirefoxNumericPref('browser.cache.offline.capacity', 1024, 1024000, 1024, 521000)
    
    setting = {'normal' : 0, 'never open any new windows' : 1, 'default' : 2 }
    browser_link_open_newwindow_restriction_t = FirefoxPrefText(_('Open Javascript popups as tabs'), 'browser.link.open_newwindow.restriction')
    browser_link_open_newwindow_restriction = FirefoxComboPref('browser.link.open_newwindow.restriction', setting)
    
    setting = {'go back' : 0, 'go forward' : 1, 'unmap' : 2 }
    browser_backspace_action_t = FirefoxPrefText(_('Redefine the Backspace button'), 'browser.backspace_action' )
    browser_backspace_action = FirefoxComboPref('browser.backspace_action', setting)
    
    setting = {'none' : 'none', 'once' : 'once', 'normal' : 'normal' }
    image_animation_mod_t = FirefoxPrefText(_('Way of animating multi-frame GIF images none'), 'image.animation_mode')
    image_animation_mod = FirefoxComboPref('image.animation_mode', setting)
     
    table = gtk.Table()
    row = 0
    def add(t, w):
        global table, row
        table.attach(t, 0, 1, row, row+1, gtk.FILL|gtk.EXPAND, gtk.FILL)
        table.attach(w, 1, 2, row, row+1, gtk.FILL, gtk.FILL)
        row += 1
    add(content_max_tokenizing_time_t,content_max_tokenizing_time)
    add(content_notify_backoffcount_t,content_notify_backoffcount)
    add(network_dnsCacheEntries_t,network_dnsCacheEntries)
    add(network_dnsCacheExpiration_t,network_dnsCacheExpiration)
    add(network_ftp_idleConnectionTimeout_t,network_ftp_idleConnectionTimeout)
    add(network_http_keep_alive_timeout_t,network_http_keep_alive_timeout)
    add(network_http_max_persistent_connections_per_proxy_t,network_http_max_persistent_connections_per_proxy)
    add(nglayout_initialpaint_delay_t,nglayout_initialpaint_delay)
    add(network_http_max_connections_t,network_http_max_connections)
    add(network_http_max_connections_per_server_t,network_http_max_connections_per_server)
    add(browser_sessionstore_max_tabs_undo_t,browser_sessionstore_max_tabs_undo)
    add(browser_blink_allowed_t,browser_blink_allowed)
    add(browser_tabs_tab_min_width_t,browser_tabs_tab_min_width)
    add(toolkit_scrollbox_scroll_increment_t,toolkit_scrollbox_scroll_increment)
    add(browser_urlbar_autofill_t,browser_urlbar_autofill)
    add(browser_bookmarks_auto_export_html_t,browser_bookmarks_auto_export_html)
    add(browser_history_expire_days_t,browser_history_expire_days)
    add(broswer_history_expire_sites_t,broswer_history_expire_sites)
    add(extension_get_addons_max_results_t,extension_get_addons_max_results)
    add(browser_cache_offline_capacity_t,browser_cache_offline_capacity)
    add(browser_link_open_newwindow_restriction_t, browser_link_open_newwindow_restriction)
    add(browser_backspace_action_t, browser_backspace_action)
    add(image_animation_mod_t, image_animation_mod)
    
    def one_key_tweak(self):
        firefox.set_str_pref('content.max.tokenizing.time', 3000000)
        firefox.set_str_pref('content.notify.backoffcount', 200)
        firefox.set_str_pref('network.dnsCacheEntries', 256)
        firefox.set_str_pref('network.dnsCacheExpiration', 86400)
        firefox.set_str_pref('network.ftp.idleConnectionTimeout', 60)
        firefox.set_str_pref('network.http.keep-alive.timeout', 30)
        firefox.set_str_pref('network.http.max-persistent-connections-per-proxy', 24)
        firefox.set_str_pref('nglayout.initialpaint.delay', 0)
        firefox.set_str_pref('network.http.max-connections', 96)
        firefox.set_str_pref('network.http.max-connections-per-server', 32)
        firefox.set_str_pref('toolkit.scrollbox.scrollIncrement', 75)
        firefox.set_str_pref('browser.blink_allowed', 'false')
        firefox.set_str_pref('browser.urlbar.autoFill', 'true')
    tweak_key = gtk.Button()
    tweak_key = image_stock_button(gtk.STOCK_APPLY, _('Auto Setting Firefox') )
    tweak_key.connect('clicked', one_key_tweak)
    table.attach(tweak_key, 1, 2, row, row+1, gtk.FILL, gtk.FILL)
    row += 1
    
   
    if firefox.support:
        return Setting(table, _('Configure Firefox'), ['firefox'])
    else:
        return None
    
def get():
    ret = []
    for f in [
            __change_kernel_swappiness,
            __change_hostname,
            __configure_firefox,
            __restart_network ]:
        try:
            a = f()
            if a: ret.append(a) # if such function is not supported, f() returns None.
        except:
            print_traceback()
    return ret
