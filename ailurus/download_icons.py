#!/usr/bin/env python

import sys, os, urllib, gtk, thread, time
from lib import *
from libu import *

class DownloadIconsWindow(gtk.Window):
    icons_pack_version = 1
    url = 'http://ailurus.googlecode.com/files/other_icons_v%s.tar.gz' % icons_pack_version
    filename = '/tmp/other_icons.tar.gz'
    
    def __init__(self):
        gtk.Window.__init__(self)
        self.urllabel = gtk.Label()
        self.urllabel.set_alignment(0, 0.5)
        self.progressbar = gtk.ProgressBar()
        vbox = gtk.VBox(False, 10)
        vbox.set_border_width(10)
        vbox.pack_start(self.urllabel)
        vbox.pack_start(self.progressbar)
        self.add(vbox)
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER)
        self.realize() # show "busy" cursor
        try: self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        except: print_traceback()
        self.connect('delete-event', self.before_delete_event)
        self.show_all()

        self.can_exit = False
        self.exception = None
        self.set_title(_('Downloading icons'))
        self.urllabel.set_text(_('Downloading:') + ' ' + self.url)
        self.progressbar.set_text('0%')
        self.percentage = 0

    def before_delete_event(self, *w):
        if self.can_exit == False: return True
        else: sys.exit()
    
    def reporthook(self, blocks_transferred, block_size, total_size):
        self.percentage = min(1, float(blocks_transferred * block_size) / total_size)

    def download_thread(self):
        try:
            urllib.urlretrieve(self.url, self.filename, self.reporthook)
            raise Exception(1,2,3)
        except:
            self.exception = sys.exc_info()
        finally:
            self.can_exit = True

    def show_percentage(self):
        self.progressbar.set_fraction(self.percentage)
        self.progressbar.set_text('%s%%' % int(self.percentage*100))
    
    def main_thread(self):
        while self.can_exit == False:
            self.show_percentage()
            while gtk.events_pending(): gtk.main_iteration()
            time.sleep(0.1)
        self.show_percentage()
        while gtk.events_pending(): gtk.main_iteration()
        if self.exception:
            exception_happened(*self.exception)
            gtk.main() # show exception dialog
        else:
            print 1 # todo

import ctypes # change_task_name
libc = ctypes.CDLL('libc.so.6')
libc.prctl(15, 'ailurus_icon_downloader', 0, 0, 0)
if get_output('pgrep -u $USER ailurus_icon_downloader', True): # detect_running_instances
    sys.exit(1) # another instance is running
gtk.gdk.threads_init()
window = DownloadIconsWindow()
thread.start_new_thread(window.download_thread, ())
gtk.gdk.threads_enter()
window.main_thread()
gtk.gdk.threads_leave()