#coding: utf-8
#
# Ailurus - a simple application installer and GNOME tweaker
#
# Copyright (C) 2009-2010, Ailurus developers and Ailurus contributors
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
from libapp import *

AMule_0 = 'aMule'
AMule_1 = _('Free peer-to-peer file sharing application that works with EDonkey network and Kad network, offering similar features to eMule')
AWN_0 = _('Avant Window Navigator')
AWN_1 = _('A dock sits at the bottom of the screen which lists open windows. It also supports third party applets.')
Agave_0 = 'Agave'
Agave_1 = _('A designer which can generate a variety of colorschemes from a single starting color')
Alacarte_0 = 'Alacarte'
Alacarte_1 = _('Edit GNOME menu easily')
Anjuta_0 = 'Anjuta'
Anjuta_1 = _('GNOME IDE for C/C++ with a number of features such as project management, application wizard, interactive debugger, source editor, version control, GUI designer and profiler.')
Artha_0 = 'Artha'
Artha_1 = _('Look up synonyms and antonyms')
Audacity_0 = 'Audacity'
Audacity_1 = _('Record and edit sounds')
AutoApt_0 = 'Auto-apt'
AutoApt_1 = _('"auto-apt run ./configure" helps you automatically install required packages.')
AutoTools_0 = _('Autoconf and Automake')
AutoTools_1 = _('Automatically generate configure scripts and GNU Standard makefiles')
Avidemux_0 = 'Avidemux'
Avidemux_1 = _('Video editor which can do simple cutting, filtering and encoding tasks. It supports scripts and automated job queue.')
Backintime_0 = 'Back In Time'
Backintime_1 = _('Incremental backup tool supporting schedule')
Banshee_0 = 'Banshee'
Banshee_1 = _('Media player and media manager written in Mono and Gtk#. It is the default media player for several Linux distribution.')
Bluefish_0 = 'Bluefish'
Bluefish_1 = _('An editor targeted towards webdesigners. It supports many programming and markup languages, and it focuses on editing dynamic websites.')
Bluez_0 = 'BlueZ'
Bluez_1 = _('Official Linux bluetooth support')
Boost_0 = _('Boost C++ libraries')
Boost_1 = _('Peer-reviewed portable C++ libraries, which will be in the new C++ 0x standard.')
BosWars_0 = _('Bos Wars')
BosWars_1 = _('Real time strategy game, just like Red Alarm')
Brasero_0 = 'Brasero'
Brasero_1 = _('A simple CD/DVD burner')
BreatheIconTheme_0 = _('Breathe Icon Theme')
BreatheIconTheme_1 = _('Mix KDE\'s "Oxygen" icons with Ubuntu\'s "Human" theme.')
Build_Essential_0 = _('g++, make, gdb and libc')
Build_Essential_1 = _('Popular development tools')
Celestia_0 = 'Celestia'
Celestia_1 = _('3D astronomy simulator')
CHMSee_Read_CHM_Documents_0 = 'ChmSee'
CHMSee_Read_CHM_Documents_1 = _('View .chm files')
CheckInstall_0 = 'CheckInstall'
CheckInstall_1 = _('Help you build .deb packages')
Cheese_0 = 'Cheese'
Cheese_1 = _('It helps you take pictures and videos from web camera. It also provides some graphical effects in order to please your play instinct.')
ChildsPlay_0 = 'ChildsPlay'
ChildsPlay_1 = _('Educational games for young children')
ClawsMail_0 = _('Claws Mail')
ClawsMail_1 = _('Lightweight email client')
CodeBlocks_0 = 'Code::Blocks'
CodeBlocks_1 = _('C/C++ IDE with many features')
Comix_0 = 'Comix'
Comix_1 = _('Image viewer specifically designed to handle comic books')
CompizSettingManager_0 = _('Compiz settings manager')
CompizSettingManager_1 = _('Full-function software which can configure all options of Compiz window manager')
CompizSettingManagerSimple_0 = 'Simple-ccsm'
CompizSettingManagerSimple_1 = _('Simple configure software for Compiz window manager')
Ctags_Cscope_0 = _('Ctags and Cscope')
Ctags_Cscope_1 = _('Popular source code parsers')
Deluge_0 = 'Deluge'
Deluge_1 = _('Lightweight bittorrent client')
Devhelp_0 = 'Devhelp'
Devhelp_1 = _('Browse GNOME/GTK API documentation')
Dia_0 = 'Dia'
Dia_1 = _('Open source substitution for Visio')
DOSBox_0 = 'DOSBox'
DOSBox_1 = _('Lightweight DOS simulator, which primarily focuses on running DOS games')
EasyTAG_0 = 'EasyTAG'
EasyTAG_1 = _('Edit tags for MP3, FLAC, Ogg files')
Emacs_0 = 'Emacs'
Emacs_1 = _('Advanced text editor')
Emesene_0 = 'Emesene'
Emesene_1 = _('MSN Messenger client with a simpler interface and a nicer look')
Empathy_0 = 'Empathy'
Empathy_1 = _('Messaging program which supports many protocols')
Enhance_Decompression_Capability_0 = _('p7zip and cabextract')
Enhance_Decompression_Capability_1 = _('compressor/decompressor for .7z and .cab files')
Evince_Read_Chinese_PDF_0 = _('Encoding data for the poppler PDF library')
Evince_Read_Chinese_PDF_1 = _('Make Evince be able to reveal Japanese, Korean, Chinese pdf')
Evolution_0 = 'Evolution'
Evolution_1 = _('Email client, calendar, contact manager and address manager')
Extcalc_0 = 'Extcalc'
Extcalc_1 = _('Multifunctional graphic calculator')
Fatrat_0 = 'Fatrat'
Fatrat_1 = _('A download manager supporting RapidShare.com, YouTube and remote control')
Fcitx_0 = 'Fcitx'
Fcitx_1 = _('Popular Chinese input method')
FileZilla_0 = 'FileZilla'
FileZilla_1 = _('Popular FTP client')
FireWall_0 = 'Firestarter'
FireWall_1 = _('Configure software for "iptables" firewall. "iptables" is the filewall which Linux system comes up with.')
FreeDOOM_0 = 'FreeDOOM'
FreeDOOM_1 = _('Open source clone of DOOM')
FreeGLut3_0 = _('OpenGL library')
FreeGLut3_1 = _('This is a library for writing OpenGL programs.')
FrozenBubble_0 = _('Frozen Bubble')
FrozenBubble_1 = _('Open source clone of the popular "Puzzle Bobble" game')
Gajim_0 = 'Gajim'
Gajim_1 = _('an light-weight XMPP client, supporting GTalk. GTK version')
GCompris_0 = 'GCompris'
GCompris_1 = _('Educational games for children aged 2 to 10')
GCstar_0 = 'GCstar'
GCstar_1 = _('Manage your collections such as movies, books, music')
GIMP_0 = 'GIMP'
GIMP_1 = _('Open source substitution for Photoshop')
Glade_0 = 'Glade'
Glade_1 = _('Visually graphical user interface designer')
GMP_0 = 'GMP'
GMP_1 = _('GNU high precision arithmetic library')
GNOMEColors_0 = _('GNOME Colors')
GNOMEColors_1 = _('A set of icons with 7 color variations')
GNOMEDo_0 = _('GNOME Do')
GNOMEDo_1 = _('Desktop launcher which helps you quickly perform actions')
GNOMEShell_0 = _('GNOME shell')
GNOMEShell_1 = _('Experience GNOME 3 desktop')
GNOME_mplayer_0 = _('GNOME MPlayer')
GNOME_mplayer_1 = _('GTK frontend for MPlayer')
Geany_0 = 'Geany'
Geany_1 = _('Lightweight text editor')
Ghex_0 = 'Ghex'
Ghex_1 = _('Hex editor')
Giver_0 = 'Giver'
Giver_1 = _('Automatically discover other people running Giver on the network, then send files to other people')
Glest_0 = 'Glest'
Glest_1 = _('Real time strategy game, just like Warcraft')
Globulation2_0 = _('Globulation 2')
Globulation2_1 = _('Real time strategy game which focuses on strategy rather than on micro-management')
Gnash_0 = 'Gnash'
Gnash_1 = _('SWF movie player for web browser')
Gnote_0 = 'Gnote'
Gnote_1 = _('Mono-free alternative to Tomboy Notes')
GoldenDict_0 = 'GoldenDict'
GoldenDict_1 = _('One of the best dictionary applications, which supports many dictionary formats of other software, and Wikipedia.')
GoogleGadgetsGTK_0 = _('Google gadgets (GTK version)')
GoogleGadgetsGTK_1 = _("Eye candy widgets most of which are developed by Google's users")
GoogleGadgetsQT_0 = _('Google gadgets (QT version)')
GoogleGadgetsQT_1 = _("Eye candy widgets most of which are developed by Google's users")
Gwibber_0 = 'Gwibber'
Gwibber_1 = _('Microblogging client which supports Twitter and Facebook')
HardwareLister_0 = 'lshw'
HardwareLister_1 = _('A small application which displays detailed hardware information')
Hedgewars_0 = 'Hedgewars'
Hedgewars_1 = _('Hedgehogs fight enemies with fantastic weapons')
ImageMagick_0 = 'ImageMagick'
ImageMagick_1 = _('Help you edit images. You can launch it by /usr/bin/display')
Inkscape_0 = 'Inkscape'
Inkscape_1 = _('Vector image designer. It is the open source substitution of CorelDraw.')
JabRef_0 = 'JabRef'
JabRef_1 = _('Bibliography reference manager. File format is BibTeX, the standard LaTeX bibliography format.')
K3B_0 = 'K3B'
K3B_1 = _('Burn DVD/VCD')
Kadu_0 = 'Kadu'
Kadu_1 = _('Popular instant messenger in Poland')
KDevelop_0 = 'KDevelop'
KDevelop_1 = _('An IDE similar to Visual Studio. It currently only supports C++. Other language supports are under development.')
Keepassx_0 = 'Keepassx'
Keepassx_1 = _('Password manager which saves many different information e.g. user names and passwords in one single database.')
Kflickr_0 = 'kflickr'
Kflickr_1 = _('Upload photos to Flickr')
Kile_0 = 'Kile'
Kile_1 = _('Probably the best LaTeX editor')
Kstars_0 = 'Kstars'
Kstars_1 = _('Planetarium software')
Kupfer_0 = 'Kupfer'
Kupfer_1 = _('Lightweight desktop launcher')
Leafpad_0 = 'Leafpad'
Leafpad_1 = _('Simple text editor')
Liferea_0 = 'Liferea'
Liferea_1 = _('Simple RSS feed reader')
LinuxDCPP_0 = 'Linuxdcpp'
LinuxDCPP_1 = _('Connect to a central hub then share files and chat with other people.')
LyX_0 = 'LyX'
LyX_1 = _('"what you see is what you mean" LaTeX editor')
MACChanger_0 = 'MACChanger'
MACChanger_1 = _('Change the MAC address of network interfaces')
Maxima_0 = 'Maxima'
Maxima_1 = _('Maxima is a system for the manipulation of symbolic and numerical expressions, including differentiation, integration, Taylor series, Laplace transforms, ordinary differential equations, systems of linear equations, polynomials, and sets, lists, vectors, matrices, and tensors.')
Midori_0 = 'Midori'
Midori_1 = _('Lightweight web browser')
MiniCom_Ckermit_0 = _('Minicom and Kermit')
MiniCom_Ckermit_1 = _('Communication software for embedded MCU boards')
Minitube_0 = 'Minitube'
Minitube_1 = _('This is a simple YouTube client. You enter a keyword, then the software will retrieve all relative URLs from YouTube and play them one after the other.')
Miro_0 = 'Miro'
Miro_1 = _('Internet TV video player')
Moonlight_0 = 'Moonlight'
Moonlight_1 = _('Open source implementation of Microsoft Silverlight. It provides Windows media codecs. You can enjoy Windows video in webpages.')
Multimedia_Codecs_0 = _('gstreamer multi-media codec')
Multimedia_Codecs_1 = _('Libraries supporting video playback, audio mixing and non-linear video editing')
Nautilus_Actions_0 = _('"Actions configuration" entry')
Nautilus_Actions_1 = _('Configure which software to be launched on selected files. This entry is in "System"->"Preferences" menu.')
Nautilus_Audio_Convert_0 = _('"Convert audio files" entry')
Nautilus_Audio_Convert_1 = _('Converts between WAV, OGG, MP3, MPC, FLAC, APE and AAC files.')
Nautilus_Filename_Repairer_0 = _('"Repair filename" entry')
Nautilus_Filename_Repairer_1 = _('When any file with wrong encoding filename is right clicked, show a "Repair filename" menu item.')
Nautilus_Gksu_0 = _('"Open as administrator" entry')
Nautilus_Gksu_1 = _('Launch selected files or open selected folder with administration privileges.')
Nautilus_Image_Converter_0 = _('"Resize/Rotate images" entries')
Nautilus_Image_Converter_1 = _('Resize or rotate selected images.')
Nautilus_Open_Terminal_0 = _('"Open in terminal" entry')
Nautilus_Open_Terminal_1 = _('Open a terminal in current folder.')
Nautilus_Script_Collection_Svn_0 = _('"Subversion commands" entries')
Nautilus_Script_Collection_Svn_1 = _('A lot of subversion management command')
Nautilus_Share_0 = _('"Share folders" entry')
Nautilus_Share_1 = _('Share folders using Samba')
Nautilus_Wallpaper_0 = _('"Set as wallpaper" entry')
Nautilus_Wallpaper_1 = _('Set an image as wallpaper using context menu')
Ncurses_and_qt3mt_0 = _('Ncurses5 and QT3')
Ncurses_and_qt3mt_1 = _('Necessary libraries for compiling Linux kernel')
Netbeans_0 = 'NetBeans'
Netbeans_1 = _('An open source IDE which supports several languages (C, C++, Java, Ruby, etc.) and frameworks (J2SE, J2ME, etc.)')
Nexuiz_0 = 'Nexuiz'
Nexuiz_1 = _('3D first-person shooter game')
Octave_0 = 'Octave'
Octave_1 = _('Matlab compatible numerical computation appliation')
OpenJDK_0 = _('OpenJDK 6')
OpenJDK_1 = _('Open source implementation of Java')
Openshot_0 = 'Openshot'
Openshot_1 = _('Popular non-linear video editor')
Parcellite_0 = 'Parcellite'
Parcellite_1 = _('This is a powerful clipboard manager. It can preserve 25 strings concurrently.')
Pdfedit_0 = 'PDFedit'
Pdfedit_1 = _('Add marks and annotations on PDF files.')
Pdftk_0 = _('PDF toolkit')
Pdftk_1 = _('A command line tool which can split, merge, encrypt and uncompress PDF files.')
PiTiVi_0 = 'PiTiVi'
PiTiVi_1 = _('Movie editor designed for both the newcomer and the professional users')
Pidgin_0 = 'Pidgin'
Pidgin_1 = _('A chat program which lets you log in multiple chat networks simultaneously. It supports many chat networks.')
Pino_0 = 'Pino'
Pino_1 = _('Twitter and Identi.ca client')
PowerTop_0 = 'PowerTop'
PowerTop_1 = _('Help you save power for your laptop.')
POSIX_ManPages_0 = _('POSIX library manual pages')
POSIX_ManPages_1 = _('Install manual pages about Linux system calls, library calls, and POSIX libraries.')
PSI_0 = 'PSI'
PSI_1 = _('An XMPP client, supporting GTalk. QT version')
QBittorrent_0 = 'qBittorrent'
QBittorrent_1 = _('Lightweight, featureful open source equivalent to utorrent')
QCad_0 = 'QCad'
QCad_1 = _('Open source substitution of AutoCAD')
QT_Creator_0 = _('Qt Creator')
QT_Creator_1 = _('Lightweight Qt IDE')
Qnapi_0 = 'Qnapi'
Qnapi_1 = _('Help you find and download Poland subtitles for given video file')
QtiPlot_0 = 'QtiPlot'
QtiPlot_1 = _('Open source substitution of Origin. It is the indispensable plotting application for writing Physics experiments reports.')
QutIM_0 = 'qutIM'
QutIM_1 = _('Lightweight messaging program')
R_Language_Basic_0 = _('R language')
R_Language_Basic_1 = _('A powerful statistical computation language and a graphics system.')
RKWard_0 = 'RKWard'
RKWard_1 = _('A graphic user interface to the R programming language')
SDL_0 = _('SDL library')
SDL_1 = _('A cross-platform multimedia library designed to provide low level access to hardware.')
SMPlayer_0 = 'SMPlayer'
SMPlayer_1 = _('Qt frontend for MPlayer')
ScienceBiology_0 = 'Med-bio'
ScienceBiology_1 = _('A lot of software for molecular biology, structural biology and bioinformatics.')
Scilab_0 = 'Scilab'
Scilab_1 = _('An open source alternatives to MATLAB. MATLAB code can be converted to Scilab.')
Screenlets_0 = 'Screenlets'
Screenlets_1 = _('Add eye candy gadgets on desktop, such as sticky notes, clocks, weather forecasts and so on.')
Scribus_0 = 'Scribus'
Scribus_1 = _('Professional typesetting software')
ShikiColors_0 = _('Shiki Colors')
ShikiColors_1 = _('Hybrid theme which is designed to be fast and stable')
Shutter_0 = 'Shutter'
Shutter_1 = _('A screenshot program. You can take a screenshot of a specific area, window, whole screen, then apply different effects to it.')
Sonata_0 = 'Sonata'
Sonata_1 = _('Lightweight music player')
Stardict_0 = 'Stardict'
Stardict_1 = _('Popular dictionary software')
StartupManager_0 = _('Startup Manager')
StartupManager_1 = _('Change GRUB settings and themes')
Svn_Git_bzr_0 = _('Subversion, Git and Bzr')
Svn_Git_bzr_1 = _('Popular version control systems')
TeXLive_0 = 'TeXLive'
TeXLive_1 = _('A popular digital typographical system which can typeset complex mathematical formulae')
TheManaWorld_0 = _('The Mana World')
TheManaWorld_1 = _('2D MMORPG')
Thunderbird_0 = 'Thunderbird'
Thunderbird_1 = _('Email client and RSS reader')
Transmission_0 = 'Transmission'
Transmission_1 = _('Lightweight bittorrent client')
TuxPaint_0 = _('Tux Paint')
TuxPaint_1 = _('Drawing software for young children three years and up')
Typespeed_0 = 'Typespeed'
Typespeed_1 = _('Type words which are flying from left to right as fast as you can')
Ubuntu_Studio_Theme_0 = _('Ubuntu Studio Theme')
Ubuntu_Studio_Theme_1 = _('A theme of Ubuntu which is aimed at audio, video and graphic enthusiast')
Unetbootin_0 = 'Unetbootin'
Unetbootin_1 = _('Creates bootable USB flash disk, install Linux on USB flash disk, and create your custom Linux edition.')
Umbrello_0 = 'Umbrello'
Umbrello_1 = _('UML modelling software')
VIM_0 = 'VIM'
VIM_1 = _('Enhanced text editor')
VLC_0 = 'VLC'
VLC_1 = _('Media player and media format converter')
VirtualBox_0 = _('VirtualBox open source edition')
VirtualBox_1 = _('It is the only professional virtual machine which is freely available under the terms of GPL.')
Vuze_Karmic_0 = 'Vuze'
Vuze_Karmic_1 = _('Help you download files via bittorrent network and search videos')
WINE_0 = 'WINE'
WINE_1 = _('This is an indispensable application for running Windows applications on Linux.')
Warsow_0 = 'Warsow'
Warsow_1 = _('3D first-person shooter game, just like DOOM')
Warzone2100_0 = _('Warzone 2100')
Warzone2100_1 = _('Real time strategy game')
Wesnoth_0 = _('Battle for Wesnoth')
Wesnoth_1 = _('A popular turn-based game')
Workrave_0 = 'Workrave'
Workrave_1 = _('The program frequently alerts you to leave computers, take micro-pauses, rest breaks and restricts you to your daily limit of using computers.')
WorldofPadman_0 = _('World of Padman: Funny shooter game')
WorldofPadman_1 = _('Funny shooter game')
Wormux_0 = 'Wormux'
Wormux_1 = _('Funny fight game on 2D maps')
Youtubedl_0 = _('Youtube-dl: Download videos from Youtube')
Youtubedl_1 = _('Run command in terminal:') + ' youtube-dl http://www.youtube.com/watch?v=VIDEO_ID'
Zhcon_0 = 'Zhcon'
Zhcon_1 = _('Help you display Chinese characters in TTY terminal. You can launch it by "zhcon --utf8".')
Zim_0 = 'Zim'
Zim_1 = _('Notebook software which helps you create a wiki to your desktop')
ProofGeneral_0 = 'Proof General'
ProofGeneral_1 = 'A generic front-end for proof assistants, based on the customizable text editor Emacs.'

