from lib import *
from libu import *
import urllib, urllib2
import gtk, pango

class ProposeLinuxSkillWindow(gtk.Window):
    def show_contact(self):
        contact = Config.get_contact()
        self.contact_entry.set_text(contact)

    def set_contact(self, value):
        Config.set_contact(value)
        self.contact_entry.set_text(value)

    def do_submit(self):
        contact = self.contact_entry.get_text()
        buffer = self.content.get_buffer()
        linux_skill = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        try:
            add_linuxskill(linux_skill, contact)
        except:
            message = _('Cannot upload Linux skill.\n'
                        'Would you please email Linux skill to Ailurus developers? Thank you!')
            dialog = gtk.MessageDialog(buttons = gtk.BUTTONS_OK,
                                       message_format = message)
            import urllib
            dict = {'subject': 'Linux_skill', 'body': linux_skill}
            url = 'mailto:homer.xing@gmail.com?' + urllib.urlencode(dict)
            email_button = url_button(url, _('Click here'))
            align = gtk.Alignment(0.5, 0.5)
            align.add(email_button)
            dialog.vbox.pack_start(align, False)
            dialog.show_all()
            dialog.run()
            dialog.destroy()
        else:
            dialog = gtk.MessageDialog(buttons = gtk.BUTTONS_OK,
                                       message_format = _('Successfully uploaded Linux skill.\n'
                                                          'Thank you very much!'))
            dialog.run()
            dialog.destroy()
            self.destroy()

        if not contact: contact = _('Anonymous')
        Config.set_contact(contact)

    def __init__(self):
        label1 = gtk.Label(_('Thank you very much!'))
        label1.set_alignment(0, 0.5)
        
        self.contact_entry = contact_entry = gtk.Entry()
        contact_entry.modify_font(pango.FontDescription('Georgia'))
        anonymous = gtk.Button(_('Anonymous'))
        anonymous.connect('clicked', lambda *w: self.set_contact(_('Anonymous')))
        contact_box = gtk.HBox(False, 5)
        contact_box.pack_start(gtk.Label(_('Name or Email:')), False)
        contact_box.pack_start(contact_entry)
        contact_box.pack_start(anonymous, False)
        
        label2 = gtk.Label(_('Linux skill:'))
        label2.set_alignment(0, 0.5)
        
        self.content = content = gtk.TextView()
        content.modify_font(pango.FontDescription('Georgia'))
        content_scroll = gtk.ScrolledWindow()
        content_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        content_scroll.set_shadow_type(gtk.SHADOW_IN)
        content_scroll.add(content)

        submit_button = gtk.Button(stock=gtk.STOCK_OK)
        submit_button.connect('clicked', lambda *w: self.do_submit())
        cancel_button = gtk.Button(stock=gtk.STOCK_CANCEL)
        cancel_button.connect('clicked', lambda *w: self.destroy())
        button_box = gtk.HBox(False, 5)
        button_box.pack_end(cancel_button, False)
        button_box.pack_end(submit_button, False)

        vbox = gtk.VBox(False, 5)
        vbox.pack_start(label1, False)
        vbox.pack_start(contact_box, False)
        vbox.pack_start(label2, False)
        vbox.pack_start(content_scroll)
        vbox.pack_start(button_box, False)
        
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title(_('Propose a Linux skill'))
        self.set_border_width(5)
        self.add(vbox)
        self.set_focus(content)
        self.set_default_size(-1, 400)
        self.show_all()
        
        self.show_contact()

if __name__ == '__main__': # test
    window = ProposeLinuxSkillWindow()
    gtk.main()