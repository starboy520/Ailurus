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

class AMule(N):
    'aMule'
    detail = _('An eMule-like client for eD2k and Kademlia networks')
    category = 'file_sharing'
    if UBUNTU or MINT: pkgs = 'amule'
    if FEDORA: pkgs = 'amule'

class AWN(N):
    __doc__ = _('AWN (Avant Window Navigator): A dock-like bar')
    license = GPL
    category = 'panel'
    if UBUNTU or MINT:
        pkgs = 'avant-window-navigator'
    if FEDORA:
        pkgs = 'avant-window-navigator'
            
class Agave(N):
    'Agave'
    detail = _('Colorscheme designer')
    category = 'drawing'
    if UBUNTU or MINT: pkgs = 'agave'
    if FEDORA: pkgs = 'agave'

class Alacarte(N):
    __doc__ = ("Alacarte: Edit GNOME menu")
    license = LGPL
    DE = 'gnome'
    if FEDORA:
        pkgs = 'alacarte'
    if UBUNTU or MINT:
        pkgs = 'alacarte'
    
class Anjuta(N):
    'Anjuta'
    detail = _('GNOME IDE for C/C++')
    category = 'ide'
    if UBUNTU or MINT: pkgs = 'anjuta'
    if FEDORA : pkgs = 'anjuta'


class Audacity(N):
    __doc__ = _('Audacity: Music editor')
    license = LGPL + ' http://audacity.sourceforge.net/'
    category = 'media_editor'
    if FEDORA:
        pkgs = 'audacity'
    if UBUNTU or MINT:
        pkgs = 'audacity'

class AutoApt(N):
    'Auto-apt'
    detail = _('"auto-apt run ./configure" can help you install the packages which are not installed.')
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'auto-apt'

class AutoTools(N):
    __doc__ = _('Autoconf and Automake: Generate configure scripts and Makefiles')
    license = GPL
    category = 'saber'
    if UBUNTU or MINT:
        pkgs = 'autoconf automake'
    if FEDORA:
        pkgs = 'autoconf automake'

class Avidemux(N):
    'Avidemux'
    detail = _('Video editor')
    category = 'media_editor'
    if UBUNTU or MINT: pkgs = 'avidemux'
    if FEDORA: pkgs = 'avidemux'


class Banshee(N):
    'Banshee'
    detail = _('Media player and media manager')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'banshee'
    if FEDORA: pkgs = 'banshee'

class Bluefish(N):
    __doc__ = _('Bluefish: Edit HTML web-pages')
    license = GPL
    category = 'saber'
    if UBUNTU or MINT:
        pkgs = 'bluefish'
    if FEDORA:
        pkgs = 'bluefish'

class Bluetooth(N):
    __doc__ = _('Bluetooth support')
    license = GPL
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'bluetooth bluez-alsa bluez-cups bluez-utils python-bluez gnome-bluetooth gnome-phone-manager'
        DE = 'gnome'
    if FEDORA:
        pkgs = 'bluez-alsa bluez-cups bluez-gstreamer pybluez gnome-bluetooth gnome-phone-manager'
        DE = 'gnome'

class Boost(N):
    __doc__ = _('Boost library')
    license = GPL
    category = 'library'
    if UBUNTU or MINT:
        pkgs = 'libboost-dev'
    if FEDORA:
        pkgs = 'boost-devel'

class BosWars(N):
    'Bos Wars'
    detail = _('Real time strategy game, just like Red Alarm')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'boswars'
    if FEDORA: pkgs = 'boswars'

class BreatheIconTheme(N):
    __doc__ = _('Breathe Icon Theme')
    detail = _("""Mix KDE's "Oxygen" icons with Ubuntu's "Human" theme.""")
    category = 'theme'
    if UBUNTU or MINT: pkgs = 'breathe-icon-theme'

class Build_Essential(N):
    'Build-essential'
    detail = _('By installing build-essential, you will get g++, make, gdb and libc.')
    category = 'saber'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'build-essential'
    if FEDORA:
        pkgs = 'gcc make gdb'

class CHMSee_Read_CHM_Documents(N) :
    __doc__ = _('ChmSee: A CHM file viewer')
    category = 'business'
    license = GPL + ' http://code.google.com/p/chmsee/'
    if FEDORA:
        pkgs = 'chmsee'
    if UBUNTU or MINT:
        pkgs = 'chmsee'

class CheckInstall(N):
    'CheckInstall'
    detail = _('Checkinstall help you build deb package.')
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'checkinstall'
        
class Cheese(N):
    __doc__ = _('Cheese')
    detail = _('Take pictures and videos from your webcam, also provides some graphical effects')
    category = 'others'
    if UBUNTU or MINT : pkgs = 'cheese'
    if FEDORA : pkgs = 'cheese'

class ChildsPlay(N):
    __doc__ = _('ChildsPlay: A suite of educational games for children')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'childsplay'
    if UBUNTU or MINT:
        def __init__(self):
            pkgs = APT.get_existing_pkgs_set()
            voices = [ e for e in pkgs if e.startswith('childsplay-alphabet-sounds-') ]
            lang = Config.get_locale().split('_')[0]
            voice = 'childsplay-alphabet-sounds-'+lang
            if not voice in voices: voice = ''
            else: voice = ' ' + voice
            self.pkgs = 'childsplay' + voice
            # There is no 'childsplay-plugins-lfc' package in Karmic :)
            # 'childsplay-plugins-lfc' is letterFlashscard game.
            if APT.exist('childsplay-plugins-lfc'):
                self.pkgs += ' childsplay-plugins-lfc'
        
class ClawsMail(N):
    'Claws Mail'
    detail = _('Lightweight email client')
    category = 'email'
    if UBUNTU or MINT: pkgs = 'claws-mail'
    if FEDORA :pkgs = 'claws-mail'
    
class CodeBlocks(N):
    __doc__ = _('Code::Blocks - C/C++ IDE')
    license = GPL
    category = 'ide'
    if UBUNTU or MINT:
        pkgs = 'codeblocks'
    if FEDORA:
        pkgs = 'codeblocks'

class Comix(N):
    'Comix'
    detail = _('Customizable image viewer specifically designed to handle comic books')
    category = 'others'
    if UBUNTU or MINT: pkgs = 'comix'
    if FEDORA : pkgs = 'comix'

class CompizSettingManager(N):
    __doc__ = _('Compiz settings manager')
    detail = _('Compiz Fusion is the unification of the Beryl project and the community around the Compiz Window Manager. '
       'Compiz settings manager is the configuration application for Compiz Fusion. '
       'It can configurate effects such as "Desktop cube" and "3D windows".')
    category = 'compiz_setting'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'compizconfig-settings-manager'
    if FEDORA : 
        pkgs = 'compiz-manager'

class CompizSettingManagerSimple(N):
    __doc__ = _('Simple-ccsm: A simple Compiz settings manager')
    category = 'compiz_setting'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'simple-ccsm'
    if FEDORA :
        pkgs = 'ccsm'
    

class Ctags_Cscope(N):
    __doc__ = _('Ctags and Cscope: Popular source code parsers')
    category = 'saber'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'exuberant-ctags cscope'
    if FEDORA:
        pkgs = 'ctags-etags cscope'

class Deluge(N):
    'Deluge'
    detail = _('Lightweight bittorrent client')
    category = 'file_sharing'
    if UBUNTU or MINT: pkgs = 'deluge'
    if FEDORA : pkgs = 'deluge'

class Devhelp(N):
    'Devhelp'
    detail = _('Browse GNOME/GTK API documentation')
    category = 'saber'
    if UBUNTU or MINT: pkgs = 'devhelp'
    if FEDORA : pkgs = 'devhelp'
    

class Dia(N):
    'Dia'
    detail = _('Open source substitution for Visio')
    category = 'drawing'
    if UBUNTU or MINT: pkgs = 'dia'
    if FEDORA : pkgs = 'dia'

class EasyTAG(N):
    'EasyTAG'
    detail = _('Edit tags for MP3, FLAC, Ogg files')
    category = 'media_editor'
    if UBUNTU or MINT: pkgs = 'easytag'
    if FEDORA : pkgs = 'easytag'

class Emacs(N):
    __doc__ = _('Emacs: Advanced text editor')
    license = GPL + ' http://www.gnu.org/software/emacs/'
    category = 'saber'
    if UBUNTU or MINT:
        pkgs = 'emacs'
    if FEDORA:
        pkgs = 'emacs'

class Emesene(N):
    'Emesene'
    detail = _('MSN Messenger client, with a simpler interface and a nicer look')
    category = 'chat'
    if UBUNTU or MINT: pkgs = 'emesene'
    if FEDORA: pkgs = 'emesene'

class Empathy(N):
    'Empathy'
    detail = _('Messaging program which supports many protocols')
    category = 'chat'
    if UBUNTU or MINT: pkgs = 'empathy'
    if FEDORA : pkgs = 'empathy'

class Enhance_Decompression_Capability(N) :
    __doc__ = _('Compression/decompression support for "*.7z" and "*.cab" files')
    if FEDORA:
        pkgs = "p7zip cabextract"
    if UBUNTU or MINT:
        pkgs = "p7zip p7zip-rar p7zip-full cabextract unace"

class Evince_Read_Chinese_PDF(N) :
    __doc__ = _('Make Evince be able to reveal Chinese, Japanese, Korean pdf')
    category='business'
    if FEDORA:
        pkgs = 'poppler-data'
    if UBUNTU or MINT:
        pkgs = 'poppler-data'

class Evolution(N):
    'Evolution'
    detail = _('Email client, calendar, contact manager and address manager')
    category = 'email'
    if UBUNTU or MINT: pkgs = 'evolution'
    if FEDORA: pkgs = 'evolution'

class Extcalc(N):
    __doc__ = _('Extcalc: A multifunctional graphic calculator')
    category = 'math'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'extcalc'
        
class Fcitx(N):
    'Fcitx'
    category = 'others'
    detail = _('This is a popular Chinese input method.\n'
               'It is from http://fcitx.googlecode.com/')
    Chinese = True
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'fcitx'
    if FEDORA:
        pkgs = 'fcitx'

class FileZilla(N):
    'FileZilla'
    detail = _('FTP client')
    category = 'file_sharing'
    if UBUNTU or MINT: pkgs = 'filezilla'
    if FEDORA : pkgs = 'filezilla'

class FireWall(N):
    __doc__ = _('Firestarter: Configure Linux firewall')
    detail = _('Linux system comes up with a firewall "iptables". '
       'Firestarter is the graphical frontend of "iptables".')
    license = GPL
    category = 'internet'
    if UBUNTU or MINT:
        pkgs = 'firestarter'   

class FreeDOOM(N):
    __doc__ = _('FreeDOOM: Open source clone of DOOM')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'freedoom'
    if FEDORA : pkgs = 'freedoom'

class FreeGLut3(N):
    __doc__ = _('OpenGL library')  
    detail = _('This is a library for writing OpenGL programs.')
    license = GPL
    category = 'library'
    if UBUNTU or MINT:
        pkgs = 'freeglut3-dev'
    if FEDORA:
        pkgs = 'freeglut-devel'

# Hide this item because more packages will be removed when remove it.
#        
#class Full_Language_Pack(N):
#    __doc__ = _('Full language support and input method')
#    detail = _('Because of live CD capacity limitation, this Linux distribution does not have full language support.\n')
#    category = 'others'
#    if UBUNTU or MINT:
#        def __init__(self):
#            import locale
#            lang = Config.get_locale().split('_')[0]
#    
#            List = [
#                    'language-pack-' + lang,
#                    'language-support-fonts-' + lang,
#                    'language-support-input-' + lang,
#                    'language-support-translations-' + lang,
#                    'language-support-' + lang,
#                    'language-support-writing-' + lang,
#                    ]
#            try:
#                get_output('pgrep -u $USER gnome-panel')
#                List.append('language-pack-gnome-' + lang)
#            except: pass
#    
#            pkgs = []
#            for p in List:
#                if APT.exist(p): pkgs.append(p)
#                
#            self.pkgs = ' '.join(pkgs)

class FrozenBubble(N):
    'Frozen Bubble'
    detail = _('Clone of the popular "Puzzle Bobble" game')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'frozen-bubble'
    if FEDORA : pkgs = 'frozen-bubble'

class GCompris(N):
    __doc__ = _('GCompris: Educational games for children aged 2 to 10')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'gcompris'
    if UBUNTU or MINT:
        def __init__(self):
            pkgs = APT.get_existing_pkgs_set()
            voices = [ e for e in pkgs if e.startswith('gcompris-sound-') ]
            lang = Config.get_locale().split('_')[0]
            voice = 'gcompris-sound-'+lang
            if not voice in voices: voice = ''
            else: voice = ' ' + voice
            self.pkgs = 'gnucap gcompris' + voice
 
class GCstar(N):
    'GCstar'
    detail = _('Manage your collections such as movies, books, music')
    category = 'business'
    if UBUNTU or MINT: pkgs = 'gcstar'
    if FEDORA : pkgs = 'gcstar'

class GIMP(N):
    'GIMP'
    detail = _('Open source substitution for Photoshop')
    category = 'drawing'
    if UBUNTU or MINT: pkgs = 'gimp'
    if FEDORA : pkgs = 'gimp'

class GMP(N):
    __doc__ = _('GNU multiprecision arithmetic library')
    category = 'library'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'libgmp3-dev'
    if FEDORA:
        pkgs = 'gmp-devel'

class GNOMEColors(N):
    'GNOME Colors'
    detail = _('A set of icons with 7 color variations')
    category = 'theme'
    if UBUNTU or MINT: pkgs = 'gnome-colors'
    if FEDORA : pkgs = 'gnome-colors-icon-theme'

class GNOMEDo(N):
    'GNOME Do'
    detail = _('Desktop launcher, which helps you quickly perform actions')
    category = 'candy'
    if UBUNTU or MINT: pkgs = 'gnome-do'
    if FEDORA : pkgs = 'gnome-do'

class GNOMEShell(N):
    'GNOME shell'
    detail = _('Experience GNOME 3 desktop')
    category = 'candy'
    if UBUNTU or MINT: pkgs = 'gnome-shell'
    if FEDORA : pkgs = 'gnome-shell'
    
class GNOME_mplayer(N):
    'GNOME MPlayer'
    detail = _('GTK frontend for MPlayer')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'gnome-mplayer'
    if FEDORA : pkgs = 'gnome-mplayer'


class Geany(N):
    'Geany'
    detail = _('Lightweight text editor')
    category = 'text_editor'
    if UBUNTU or MINT: pkgs = 'geany'
    if FEDORA : pkgs = 'geany'


class Ghex(N):
    'Ghex'
    detail = _('Hex editor')
    category = 'text_editor'
    if UBUNTU or MINT: pkgs = 'ghex'
    if FEDORA: pkgs = 'ghex'

class Giver(N):
    'Giver'
    detail = _('Automatically discover other people running Giver on the network, then send files to other people')
    category = 'file_sharing'
    if UBUNTU or MINT: pkgs = 'giver'
    if FEDORA : pkgs = 'giver'

class Glest(N):
    'Glest'
    detail = _('Real time strategy game, just like Warcraft')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'glest'
    if FEDORA : pkgs = 'glest'

class Globulation2(N):
    'Globulation 2'
    detail = _('Real time strategy game which focuses on strategy rather than on micro-management')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'glob2'
    if FEDORA : pkgs = 'glob2'

class Gnash(N):
    __doc__ = _('Flash plugin for web browser')
    category = 'flash'
    license = GPL
    if FEDORA:
        pkgs = 'gnash gnash-plugin'
    if UBUNTU or MINT:
        pkgs = 'gnash mozilla-plugin-gnash'
    
class Gnote(N):
    'Gnote'
    detail = _('Mono-free alternative to Tomboy Notes')
    category = 'business'
    if UBUNTU or MINT: pkgs = 'gnote'
    if FEDORA : pkgs = 'gnote'

class GoogleGadgetsGTK(N):
    __doc__ = _('Google gadgets') + ' ' + _('(GTK version)')
    category = 'candy'
    if UBUNTU or MINT: pkgs = 'google-gadgets-gtk'
    if FEDORA : pkgs = 'google-gadgets-gtk'

class GoogleGadgetsQT(N):
    __doc__ = _('Google gadgets') + ' ' + _('(QT version)')
    category = 'candy'
    if UBUNTU or MINT: pkgs = 'google-gadgets-qt'
    if FEDORA : pkgs = 'google-gadgets-qt'

class Gwibber(N):
    'Gwibber'
    detail = _('Microblogging client which supports Twitter and Facebook')
    category = 'blog'
    if UBUNTU or MINT: pkgs = 'gwibber'
    if FEDORA : pkgs = 'gwibber'

class HardwareLister(N):
    __doc__ = _('lshw: List hardware information')
    detail = _('A small application which displays detailed hardware information')
    license = GPL
    category = 'others'
    if FEDORA:
        pkgs = 'lshw lshw-gui'
    if UBUNTU or MINT:
        pkgs = 'lshw lshw-gtk'

class Hedgewars(N):
    'Hedgewars'
    detail = _('Hedgehogs fight enemies with fantastic weapons')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'hedgewars'
    if FEDORA : pkgs = 'hedgewars'

class ImageMagick(N):
    __doc__ = _('ImageMagick: Edit images')
    detail = _('You can start it by /usr/bin/display')
    category = 'drawing'
    if FEDORA:
        pkgs = 'ImageMagick'
    if UBUNTU or MINT:
        pkgs = 'imagemagick'
        
class Inkscape(N):
    __doc__ = _('Inkscape: Design vector image. Open source substitution of CorelDraw.')
    category = 'drawing'
    if UBUNTU or MINT: pkgs = 'inkscape'
    if FEDORA: pkgs = 'inkscape'

class K3B(N):
    __doc__ = _('K3B: Create DVD/VCD')
    category = 'cd_burner'
    if UBUNTU or MINT: pkgs = 'k3b'
    if FEDORA: pkgs = 'k3b'

class Kadu(N):
    __doc__ = 'Kadu'
    detail = _('Kadu is an instant messenger, which is very popular in Poland.\n'
               'Command : yum install kadu')
    category = 'chat'
    license = GPL
    if FEDORA:
        pkgs = 'kadu'
    if UBUNTU or MINT:
        pkgs = 'kadu'
    def visible(self):
        return Config.is_Poland_locale()

class Keepassx(N):
    'Keepassx'
    detail = _('Password manager which saves many different information e.g. user names and passwords in one single database.')
    category = 'business'
    if UBUNTU or MINT: pkgs = 'keepassx'
    if FEDORA : pkgs = 'keepassx'

class Kflickr(N):
    'kflickr'
    detail = _('Upload photos to Flickr')
    category = 'others'
    if UBUNTU or MINT: pkgs = 'kflickr'
    if FEDORA : pkgs = 'kflickr'

class Kupfer(N):
    'Kupfer'
    detail = _('Lightweight desktop launcher')
    category = 'candy'
    if UBUNTU or MINT: pkgs = 'kupfer'
    
class Leafpad(N):
    'Leafpad'
    detail = _('Simple text editor')
    category = 'text_editor'
    if UBUNTU or MINT: pkgs = 'leafpad'
    if FEDORA : pkgs = 'leafpad'


class Liferea(N):
    __doc__ = _('Liferea: a RSS feed reader')
    detail = _('This is a simple and easy used RSS feed reader.')
    license = GPL
    category = 'rss'
    if FEDORA:
        pkgs = 'liferea'
    if UBUNTU or MINT:
        pkgs = 'liferea'

class LinuxDCPP(N):
    'Linuxdcpp'
    detail = _('Connect to a central hub then share files and chat with other people.')
    category = 'file_sharing'
    if UBUNTU or MINT: pkgs = 'linuxdcpp'
    if FEDORA : pkgs = 'linuxdcpp'

class MACChanger(N):
    __doc__ = _('MACChanger: change MAC address')
    detail = _('MACChanger is a utility for viewing/manipulating the MAC address of network interfaces.')
    license = GPL
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'macchanger'
    if FEDORA:
        pkgs = 'macchanger'

class Midori(N):
    'Midori'
    detail = _('Lightweight web browser')
    category = 'browser'
    if UBUNTU or MINT: pkgs = 'midori'
    if FEDORA : pkgs = 'midori'

class MiniCom_Ckermit(N):
    __doc__ = _('Minicom and Kermit: Communication software for embedded MCU boards')
    license = GPL
    category = 'embedded_system'
    if UBUNTU or MINT:
        pkgs = 'minicom ckermit'

class Minitube(N):
    'Minitube'
    detail = _('Simple Youtube client')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'minitube'
    
class Miro(N):
    'Miro'
    detail = _('Video player')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'miro'
    if FEDORA : pkgs ='Miro'

class Moonlight(N):
    __doc__ = _(u'Moonlight: an open source implementation of Microsoft® Silverlight')
    detail = _(u'Moonlight provides Windows® media codecs. '
       u'By this application, you can enjoy Windows® video/audio in webpages.')
    license = ('Moonlight 2.0 is licensed under LGPL and MIT X11 licenses. '
               'Moonlight 1.0 is licensed under LGPL. '
               'See http://www.mono-project.com/Moonlight')
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'moonlight-plugin-mozilla'


class Multimedia_Codecs (N) :
    __doc__ = _('Multi-media codec')
    category = 'others'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = ( 'gstreamer0.10-fluendo-mp3 gstreamer0.10-ffmpeg gstreamer0.10-plugins-bad ' +
                 'gstreamer0.10-plugins-bad-multiverse gstreamer0.10-plugins-ugly gstreamer0.10-plugins-ugly-multiverse'
    )
    if FEDORA: pkgs = 'gstreamermm'

class Nautilus_Actions(N):
    __doc__ = _('"Actions configuration" entry')
    detail = _('It allows the configuration of programs to be launched on files selected.\n'
               '<span color="red">This entry is not in context menu. It is in "System"->"Preferences" menu.</span>')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if FEDORA:
        pkgs = 'nautilus-actions'
    if UBUNTU or MINT:
        pkgs = 'nautilus-actions'
        
class Nautilus_Audio_Convert(N):
    __doc__ = _('"Convert audio files" entry')
    detail = _('Converts between WAV, OGG, MP3, MPC, FLAC, APE and AAC files.\n'
               'These packages will also be installed: \n'
               '<i>lame libid3-3.8.3-dev flac faac faad mppenc</i>')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if UBUNTU or MINT:
        pkgs = 'nautilus-script-audio-convert lame libid3-3.8.3-dev flac faac faad mppenc'
        def install(self):
            N.install(self)
            if not APT.installed('nautilus-script-manager'):
                APT.install('nautilus-script-manager')
            run('nautilus-script-manager enable ConvertAudioFile')


class Nautilus_Filename_Repairer(N):
    __doc__ = _('"Repair filename" entry')
    detail = _('When any file with wrong encoding filename is right clicked,\n show a "Repair filename" menu item.')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if UBUNTU or MINT:
        pkgs = 'nautilus-filename-repairer'

class Nautilus_Gksu(N):
    __doc__ = _('"Open as administrator" entry')
    detail = _('Launch selected files with administration privileges using the context menu.\nOpen selected folder with administration privileges.')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if UBUNTU or MINT:
        pkgs = 'nautilus-gksu'
    if FEDORA: 
        pkgs = 'nautilus-beesu-manage'

class Nautilus_Image_Converter(N):
    __doc__ = _('"Resize/Rotate images" entries')
    detail = _('Resize or rotate selected images.')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if FEDORA:
        pkgs = 'nautilus-image-converter'
    if UBUNTU or MINT:
        pkgs = 'nautilus-image-converter'
        
class Nautilus_Open_Terminal(N):
    __doc__ = _('"Open in terminal" entry')
    detail = _('Open a terminal in current folder.')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if FEDORA:
        pkgs = 'nautilus-open-terminal'
    if UBUNTU or MINT:
        pkgs = 'nautilus-open-terminal'
        
class Nautilus_Script_Collection_Svn(N):
    __doc__ = _('"Subversion commands" entries')
    detail = _('"Subversion commands" entries')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if UBUNTU or MINT:
        pkgs = 'nautilus-script-collection-svn'
        def install(self):
            N.install(self)
            if not APT.installed('nautilus-script-manager'):
                APT.install('nautilus-script-manager')
            run('nautilus-script-manager enable Subversion')
        
class Nautilus_Search_Tool(N):
    __doc__ = _('"Search files" entries')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if FEDORA:
        pkgs = 'nautilus-search-tool'

class Nautilus_Share(N):
    __doc__ = _('"Share folders" entry')
    detail = _('Share folders by Samba.')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if UBUNTU or MINT:
        pkgs = 'nautilus-share'
        
class Nautilus_Wallpaper(N):
    __doc__ = _('"Set as wallpaper" entry')
    detail = _('"Set as wallpaper" entry')
    license = GPL
    category = 'nautilus_extension'
    DE = 'gnome'
    if UBUNTU or MINT:
        pkgs = 'nautilus-wallpaper'

class Ncurses_and_qt3mt(N):
    __doc__ = _('Ncurses5 and QT3')
    detail = _('libncurses5 is a library controlling writing to the console screen.\n'
               'libqt3-mt is Trolltech Qt library, version 3.') 
    license = GPL
    category = 'library'
    if UBUNTU or MINT:
        pkgs = 'libncurses5-dev libqt3-mt-dev'
    if FEDORA:
        pkgs = 'ncurses-devel qt3-devel'
        
class Netbeans(N):
    __doc__ = 'NetBeans'
    detail = (
              _('It is an open source IDE which supports several languages (C, C++, Java, Ruby, etc.)'
               ' and frameworks (J2SE, J2ME, etc.). '
               'Official site: http://netbeans.org/downloads/ .') +
              _(' This application depends on Java.') )
    category = 'ide'
    license = DUAL_LICENSE(CDDL, GPL) + ' http://netbeans.org/about/legal/license.html'
    if UBUNTU or MINT:
        pkgs = 'netbeans'
    if FEDORA:
        pkgs = 'netbeans'

class Nexuiz(N):
    'Nexuiz'
    detail = _('3D first-person shooter game')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'nexuiz'
    if FEDORA : pkgs = 'nexuiz'
    
class Octave(N):
    __doc__ = _(u'Octave: A Matlab® compatible numerical computation appliation')
    license = GPL + ' http://www.gnu.org/software/octave/license.html'
    category = 'math'
    if FEDORA:
        pkgs = 'qtoctave'
    if UBUNTU or MINT:
        pkgs = 'qtoctave'

class Openshot(N):
    'Openshot'
    detail = _('Non-linear video editor')
    category = 'media_editor'
    if UBUNTU or MINT: pkgs = 'openshot'

class POSIX_ManPages(N):
    __doc__ = _('POSIX library manual pages')
    detail = _('Install manual pages about Linux system calls, library calls, and POSIX libraries.')
    category = 'saber'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'manpages-dev manpages-posix manpages-posix-dev'

class Parcellite(N):
    __doc__ = _('Parcellite: clipboard manager')
    detail = _('This is a powerful clipboard manager. '
               'It can preserve 25 strings concurrently.')
    license = GPL
    if FEDORA:
        pkgs = 'parcellite'
    if UBUNTU or MINT:
        pkgs = 'parcellite'

class PiTiVi(N):
    __doc__ = _('PiTiVi: Movie editor')
    license = LGPL + ' http://www.pitivi.org/'
    category = 'media_editor'
    if FEDORA:
        pkgs = 'pitivi'
    if UBUNTU or MINT:
        pkgs = 'pitivi'

class Pidgin(N):
    'Pidgin'
    category = 'chat'
    if UBUNTU or MINT: pkgs = 'pidgin'
    if FEDORA: pkgs = 'pidgin'

class PowerTop(N):
    'PowerTop'
    detail = _('Powertop helps you save power for your laptop.')
    license = GPL
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'powertop'
    if FEDORA:
        pkgs = 'powertop'
        
class QCad(N):
    __doc__ = _('QCad: A CAD software which supports DXF-format')
    license = GPL
    category = 'mechanics'
    if FEDORA:
        pkgs = 'qcad'
    if UBUNTU or MINT:
        pkgs = 'qcad'
        
class QT_Creator(N):
    'Qt Creator'
    detail = _('This is an IDE for Qt.')
    category = 'ide'
    license = GPL
    if FEDORA:
        pkgs = 'qt-creator'
    if UBUNTU or MINT:
        pkgs = 'qtcreator'

class Qnapi(N):
    __doc__ = 'Qnapi'
    detail = _('QNapi is unofficial free clone of NAPI-PROJEKT program. '
                'Its purpose is to find and download subtitles for given video file. Currently only Polish subtitles are available.')
    license = GPL
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'qnapi'
        def visible(self):
            return Config.is_Poland_locale()

class QtiPlot(N) :
    __doc__ = _('QtiPlot: The equivalence of "Origin" plotting application in Linux')
    detail = _('It is the indispensable plotting application for writing Physics experiments reports.')
    category = 'math'
    license = GPL
    if FEDORA:
        pkgs = 'qtiplot'
    if UBUNTU or MINT:
        pkgs = 'qtiplot'

class QutIM(N):
    'qutIM'
    detail = _('Lightweight messaging program')
    category = 'chat'
    if UBUNTU or MINT: pkgs = 'qutim'
    if FEDORA : pkgs = 'qutim'

class R_Language_Basic(N):
    __doc__ = _('R language (basic development environment)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/')
    category = 'statistics'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'r-base-core'

class R_Language_Full(N):
    __doc__ = _('R language (full development environment and all plugins)')
    detail = _('A powerful statistical computation language and a graphics system.\n'
               'If you want to use the latest version of R language, please read http://cran.r-project.org/')
    category = 'statistics'
    license = GPL
    if UBUNTU or MINT:
        def __init__(self):
            import StringIO
            value = StringIO.StringIO()
            print >>value, 'r-base-core',
            for p in APT.get_existing_pkgs_set():
                if p.startswith('r-cran-'): print >>value, p,
            self.pkgs = value.getvalue()

class SDL(N):
    __doc__ = _('SDL library')
    detail = _('This is a library for writing SDL programs.\n'
               'SDL is a cross-platform multimedia library designed to provide low level access to audio'
               ' keyboard, mouse, joystick, 3D hardware via OpenGL, and 2D video framebuffer.')
    category = 'library'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = 'libsdl1.2-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev'
    if FEDORA:
        pkgs = 'SDL-devel SDL_gfx SDL_ttf SDL_mixer'

class SMPlayer(N):
    'SMPlayer'
    detail = _('Qt frontend for MPlayer')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'smplayer'
    if FEDORA : pkgs = 'smplayer'

class ScienceBiology(N):
    __doc__ = _('Med-bio: A lot of micro-biology software')
    detail = _('A lot of software for molecular biology, structural biology and bioinformatics.')
    category = 'biology'
    license = DUAL_LICENSE(EPL, GPL)
    if UBUNTU or MINT:
        pkgs = 'med-bio'

class Screenlets(N):
    __doc__ = _('Screenlets: Add eye candy gadgets on desktop')
    detail = _('Screenlets is able to add eye candy gadgets on desktop, '
       'such as sticky notes, clocks, weather forecasts, calendars and so on, '
       'in order to decorate the desktop.')
    category = 'candy'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'screenlets'

class Scribus(N):
    'Scribus'
    detail = _('Professional typesetting software')
    category = 'typesetting'
    if UBUNTU or MINT: pkgs = 'scribus'
    if FEDORA : pkgs = 'scribus'

class ShikiColors(N):
    'Shiki Colors'
    detail = _('Hybrid theme which is designed to be fast and stable')
    category = 'theme'
    if UBUNTU or MINT: pkgs = 'shiki-colors'
    
class Shutter(N):
    'Shutter'
    detail = _('Make screenshots')
    category = 'others'
    if UBUNTU or MINT: pkgs = 'shutter'
    if FEDORA : pkgs = 'shutter'

class Sonata(N):
    'Sonata'
    detail = _('Lightweight music player')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'sonata'
    if FEDORA: pkgs = 'sonata'

class Stardict(N):
    __doc__ = _('Stardict')
    category = 'business'
    license = GPL
    if FEDORA:
        detail = _('You can install these dictionaries by yum.\n'
                   'stardict-dic-cs_CZ: Czech dictionaries\n'
                   'stardict-dic-en: English dictionaries\n'
                   'stardict-dic-hi: Hindi dictionary\n'
                   'stardict-dic-ja: Japanese dictionaries\n'
                   'stardict-dic-ru: Russian dictionaries\n'
                   'stardict-dic-zh_CN: Simplified Chinese dictionaries\n'
                   'stardict-dic-zh_TW: Traditional Chinese dictionaries')
        pkgs = 'stardict'
    if UBUNTU or MINT:
        pkgs = 'stardict'

class StartupManager(N):
    __doc__ = _('Startup Manager: Change GRUB settings and themes')   
    detail = _('Startup manager helps you change GRUB settings and themes.')
    license = GPL
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'startupmanager'
        
class Svn_Git_bzr(N):
    __doc__ = _('Subversion, Git and Bzr: Popular version control systems')
    license = GPL
    category = 'version_control'
    if UBUNTU or MINT:
        pkgs = 'subversion git-core bzr'
    if FEDORA:
        pkgs = 'subversion git bzr'
        
class TeXLive(N):
    'TeXLive'
    detail = _('Create a file "example.tex", then compile it by "xelatex example.tex".') + ' http://ailurus.cn/?p=329'
    category = 'latex'
    if UBUNTU or MINT:
        pkgs = 'texlive-xetex texlive lmodern'
    if FEDORA:
        pkgs = 'texlive-xetex texlive-latex texlive'

class TheManaWorld(N):
    __doc__ = _('The Mana World')
    detail = _('2D MMORPG')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'tmw'
    if FEDORA : pkgs = 'manaworld'
    
class Thunderbird(N):
    'Thunderbird'
    detail = _('Email client and RSS reader')
    category = 'email'
    if UBUNTU or MINT: pkgs = 'thunderbird'
    if FEDORA : pkgs ='thunderbird'

class Transmission(N):
    'Transmission'
    detail = _('Lightweight bittorrent client')
    category = 'file_sharing'
    if UBUNTU or MINT: pkgs = 'transmission'
    if FEDORA : pkgs = 'transmission'

class TuxPaint(N):
    __doc__ = _('Tux Paint: A drawing program for young children three years and up')
    category = 'education'
    license = GPL
    if FEDORA:
        pkgs = 'tuxpaint'
    if UBUNTU or MINT:
        pkgs = 'tuxpaint'

class Typespeed(N) :
    'Typespeed'
    detail= _('Typespeed is a typing practise. It only runs in terminal.')
    category = 'game'
    license = LGPL
    if UBUNTU or MINT:
        pkgs = "typespeed"
    if FEDORA:
        pkgs = 'typespeed'

class Ubuntu_Studio_Theme(N):
    __doc__ = _('Ubuntu Studio Theme')
    license = GPL
    category = 'theme'
    if UBUNTU or MINT:
        pkgs = 'ubuntustudio-theme ubuntustudio-icon-theme ubuntustudio-wallpapers ubuntustudio-gdm-theme'
    
class Umbrello(N):
    __doc__ = _('Umbrello: UML modelling')
    detail = _('Umbrello help you do UML modelling.')
    license = GPL
    category = 'saber'
    if UBUNTU or MINT:
        pkgs = 'umbrello'

class VIM(N) :
    'VIM'
    license = GPL
    category = 'saber'
    if FEDORA:
        pkgs = 'vim-enhanced'
    if UBUNTU or MINT:
        pkgs = 'vim'

class VLC(N):
    'VLC'
    detail = _('Media player and media format converter')
    category = 'player'
    if UBUNTU or MINT: pkgs = 'vlc'
    if FEDORA : pkgs = 'vlc'

class VirtualBox(N):
    __doc__ = _('VirtualBox open source edition')
    detail = _('It is the only professional virtual machine which is freely available '
       'under the terms of GPL. '
       'Official site: http://www.virtualbox.org/wiki/Downloads')
    license = GPL
    category = 'simulator'
    if UBUNTU or MINT:
        pkgs = 'virtualbox-ose' 
    if FEDORA :
        pkgs = 'VirtualBox-OSE'

class Vuze_Karmic(N):
    # Latest Vuze is in 9.10 repository.
    __doc__ = _('Vuze: Download via bittorrent; Search videos')
    category = 'file_sharing'
    license = GPL
    if UBUNTU or MINT:
        pkgs = 'vuze'
        def visible(self):
            return VERSION not in ['hardy', 'intrepid', 'jaunty']

class WINE(N):
    __doc__ = _('WINE')
    detail = _('This is an indispensable application for running Windows applications on Linux.')
    license = LGPL + ' http://wiki.winehq.org/Licensing'
    category = 'simulator'
    if FEDORA:
        pkgs = 'wine'
    if UBUNTU or MINT:
        def __init__(self):
            if APT.exist('wine1.2') and APT.exist('wine1.2-gecko'):
                self.pkgs = 'wine1.2 wine1.2-gecko'
            else:
                self.pkgs = 'wine wine-gecko'

class Warsow(N):
    'Warsow'
    detail = _('3D first-person shooter game, just like DOOM')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'warsow'

class Warzone2100(N):
    'Warzone 2100'
    detail = _('Real time strategy game')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'warzone2100'
    if FEDORA :
        pkgs = 'warzone2100'

class Wesnoth(N):
    __doc__ = _('Battle for Wesnoth')
    detail = _('A popular turn-based game')
    category = 'game'
    if UBUNTU or MINT:
        def __init__(self):
            if APT.exist('wesnoth-1.8'): self.pkgs = 'wesnoth-1.8'
            else: self.pkgs = 'wesnoth'
    if FEDORA:
        pkgs = 'wesnoth'

class Workrave(N) :
    'Workrave'
    detail = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.')
    license = GPL + ' http://sourceforge.net/projects/workrave/'
    if FEDORA:
        pkgs = 'workrave'  
    if UBUNTU or MINT:
        pkgs = 'workrave'

class WorldofPadman(N):
    __doc__ = _('World of Padman: Funny shooter game')
    detail = _('Ailurus will install the game, and apply the latest patch.\n'
               'Download from ftp://ftp.snt.utwente.nl/pub/games/worldofpadman/linux/')
    license = GPL + ' http://sourceforge.net/projects/wop-engine/'
    category = 'others'
    if FEDORA:
        pkgs = 'worldofpadman'

class Wormux(N):
    'Wormux'
    detail = _('Funny fight game on 2D maps')
    category = 'game'
    if UBUNTU or MINT: pkgs = 'wormux'
    if FEDORA :
        pkgs = 'wormux'

class Zhcon(N):
    __doc__ = _('Zhcon')
    detail = _('Zhcon helps you display Chinese characters in TTY terminal.\n'
               'You can launch it by "zhcon --utf8".')
    Chinese = True
    license = GPL
    category = 'others'
    if UBUNTU or MINT:
        pkgs = 'zhcon'
    if FEDORA :
        pkgs = 'zhcon'

class Zim(N):
    'Zim'
    detail = _('Notebook software which helps you create a wiki to your desktop')
    category = 'business'
    if UBUNTU or MINT: pkgs = 'zim'
    if FEDORA: pkgs = 'Zim'
    
class Eclipse_CDT(N):
    __doc__ = _('CDT: C/C++ development')
    category = 'eclipse_extension'
    license = EPL + ' http://www.eclipse.org/legal/'
    if FEDORA: pkgs = 'eclipse-cdt'

class Eclipse_Pydev(N):
    __doc__ = _('Pydev: Python development')
    category = 'eclipse_extension'
    license = EPL + ' http://pydev.org/about.html'
    if FEDORA: pkgs = 'eclipse-pydev'

class Eclipse_Phpeclipse(N):
    __doc__ = _('Phpeclipse: PHP development')
    category = 'eclipse_extension'
    license = CPL + 'http://www.eclipse.org/legal/cpl-v10.html'
    if FEDORA: pkgs = 'eclipse-phpeclipse'

class Eclipse_Subversive(N):
    __doc__ = _('Subversive: Use SVN in Eclipse')
    category = 'eclipse_extension'
    license = EPL    
    if FEDORA: pkgs = 'eclipse-subclipse'
    
class Eclipse_VEditor(N):
    __doc__ = _('VEditor: Verilog and VHDL editor')
    category = 'eclipse_extension'
    license = EPL + 'http://veditor.sourceforge.net/index.html'
    if FEDORA: pkgs = 'eclipse-veditor'
    
class Eclipse_Photran(N):
    __doc__ = _('Photran: Fortran development')
    category = 'eclipse_extension'
    license = EPL + 'http://www.eclipse.org/photran/'
    if FEDORA: pkgs = 'eclipse-photran'
    
class Eclipse_Texlipse(N):
    __doc__ = _('Texlipse: Eclipse plugin for editing Latex')
    category = 'eclipse_extension'
    license = EPL + 'http://eclipse-plugins.2y.net/eclipse/plugin_details.jsp?id=992'
    if FEDORA: pkgs = 'eclipse-texlipse'    

class Eclipse_DLTK_Ruby(N):
    __doc__ = ('DLTK Ruby: Ruby development')
    category = 'eclipse_extension'
    license = EPL + 'http://marketplace.eclipse.org/content/dltk-ruby'
    if FEDORA: pkgs = 'eclipse-dltk-ruby'
    
