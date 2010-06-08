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
from lib import *

def __set1():
    return [
['AR', 'i386', 'http://fedora.patan.com.ar/linux'],
['AT', 'Zero42', 'http://fedora.zero42.at/linux'],
['AU', 'Bigpond', 'http://ga13.files.bigpond.com:4040/fedora/linux'],
['AU', 'Bigpond', 'http://ga14.files.bigpond.com:4040/fedora/linux'],
['AU', 'AARNet Mirror', 'http://mirror.aarnet.edu.au/pub/fedora/linux'],
['AU', 'Internode', 'http://mirror.internode.on.net/pub/fedora/linux'],
['AU', 'iinet.net.au', 'http://ftp.iinet.net.au/pub/fedora/linux'],
['AU', 'OptusNet', 'http://mirror.optus.net/fedora/linux'],
['AU', 'monash.edu.au', 'http://ringtail.its.monash.edu.au/pub/fedora/linux'],
['BG', 'fedora.linuxman.biz', 'http://fedora.linuxman.biz/linux'],
['BR', 'fedora.c3sl.ufpr.br', 'http://fedora.c3sl.ufpr.br/linux'],
['BR', 'mirror.ispbrasil.com.br', 'http://mirror.ispbrasil.com.br/fedora'],
['BR', 'fedora.pop.com.br', 'http://fedora.pop.com.br/linux'],
['CA', 'NRC', 'ftp://ftp.nrc.ca/pub/systems/linux/redhat/fedora/linux'],
['CA', 'iWeb Technologies inc.', 'http://fedora.mirror.iweb.ca'],
['CA', 'ftp.muug.mb.ca', 'http://www.muug.mb.ca/pub/fedora/linux'],
['CA', 'University of Calgary', 'http://mirror.cpsc.ucalgary.ca/mirror/fedora/linux'],
['CH', 'SWITCHmirror', 'http://mirror.switch.ch/ftp/mirror/fedora/linux'],
['CN', 'sohu mirror', 'http://mirrors.sohu.com/fedora'],
['CN', '163.com', 'http://mirrors.163.com/fedora'],
['CR', 'mirrorsucr', 'http://mirrors.ucr.ac.cr/fedora'],
['CY', 'Cytanet Mirror', 'http://mirrors.cytanet.com.cy/linux/fedora/linux'],
['CZ', 'sunsite.mff.cuni.cz', 'http://ultra.linux.cz/MIRRORS/fedora.redhat.com/linux'],
['CZ', 'Masaryk University, Brno', 'http://ftp.linux.cz/pub/linux/fedora/linux'],
['CZ', 'Silicon Hill', 'http://ftp.sh.cvut.cz/MIRRORS/fedora/linux'],
['CZ', 'mirror.karneval.cz', 'http://mirror.karneval.cz/pub/linux/fedora/linux'],
['DE', 'fedora.tu-chemnitz.de', 'http://fedora.tu-chemnitz.de/pub/linux/fedora/linux'],
['DE', 'uni-kl.de', 'http://ftp.uni-kl.de/pub/linux/fedora/linux'],
['DE', 'ftp-stud.hs-esslingen.de', 'http://ftp-stud.hs-esslingen.de/pub/fedora/linux'],
['DE', 'ATrpms', 'http://mirror2.atrpms.net/fedora/linux'],
['DE', 'SunSITE CEUR', 'http://sunsite.informatik.rwth-aachen.de/ftp/pub/Linux/fedora/linux'],
['DE', 'ATrpms', 'http://mirror1.atrpms.net/fedora/linux'],
['DE', 'Uni Bayreuth', 'http://ftp.uni-bayreuth.de/linux/fedora/linux'],
['DE', 'Universität Oldenburg', 'http://fedora.uni-oldenburg.de'],
['DE', 'STW Bonn', 'http://ftp.stw-bonn.de/pub/fedora/linux'],
['DE', 'Universität zu Köln', 'http://ftp.uni-koeln.de/mirrors/fedora/linux'],
['DE', 'Informatik Uni-Frankfurt, Germany', 'http://ftp.informatik.uni-frankfurt.de/fedora'],
['DE', 'Fraunhofer', 'http://mirror.fraunhofer.de/download.fedora.redhat.com/fedora/linux'],
['DE', 'Univ. of Erlangen-Nürnberg (FAU)', 'http://ftp.uni-erlangen.de/pub/Linux/MIRROR.fedora/core'],
['DE', 'mirror.andreas-mueller.com', 'http://mirror.andreas-mueller.com/pub/fedora/linux'],
['DK', 'crc.dk', 'http://ftp.crc.dk/fedora/linux'],
['DK', 'ftp.klid.dk', 'http://ftp.klid.dk/ftp/fedora/linux'],
['EE', 'redhat.linux.ee', 'http://redhat.linux.ee/pub/fedora/linux'],
['ES', 'Oficina de Software Libre de la Universidad de la Coruña (OSL UDC)', 'http://ftp.udc.es/fedora/linux'],
['ES', 'Instituto de Robotica/Universidad de Valencia', 'http://mirror.uv.es/mirror/fedora/linux'],
['ES', 'Universitat de Lleida', 'http://ftp.udl.es/pub/fedora/linux'],
['ES', 'Grupo Universitario de Informática (Universidad de Valladolid)', 'http://ftp.gui.uva.es/sites/fedora.redhat.com/linux'],
['FI', 'ftp.funet.fi', 'http://ftp.funet.fi/pub/mirrors/fedora.redhat.com/pub/fedora/linux'],
['FR', 'Free', 'ftp://ftp.free.fr/mirrors/fedora.redhat.com/fedora/linux'],
['FR', 'OVH', 'http://mirror.ovh.net/download.fedora.redhat.com/linux'],
['FR', 'Ircam', 'http://mirrors.ircam.fr/pub/fedora/linux'],
['FR', 'University Of Nantes', 'http://fedora.univ-nantes.fr/fedora.redhat.com/fedora/linux'],
['FR', 'LIP6', 'http://ftp.lip6.fr/ftp/pub/linux/distributions/fedora'],
['FR', 'CIRIL', 'ftp://ftp.ciril.fr/pub/linux/fedora/linux'],
['FR', 'fr2.rpmfind.net', 'http://fr2.rpmfind.net/linux/fedora'],
['FR', 'cru', 'ftp://ftp.cru.fr/pub/linux/fedora'],
['FR', 'fr.rpmfind.net', 'http://fr.rpmfind.net/linux/fedora'],
['GB', 'University of Kent UK Mirror Service', 'http://www.mirrorservice.org/sites/download.fedora.redhat.com/pub/fedora/linux'],
['GB', 'Bytemark Hosting', 'http://mirror.bytemark.co.uk/fedora/linux'],
['GB', 'Goscomb Technologies Limited', 'http://mirror.sov.uk.goscomb.net/fedora/linux'],
['GE', 'mirror.alva.ge', 'http://mirror.alva.ge/pub/fedora'],
['GR', 'NTUA', 'http://ftp.ntua.gr/pub/linux/fedora/linux'],
['GR', 'Computer Centre - UoC', 'http://ftp.cc.uoc.gr/pub/fedora/linux'],
['HK', 'CUHK', 'http://ftp.cuhk.edu.hk/pub/linux/fedora'],
['IE', 'HEAnet', 'http://ftp.heanet.ie/pub/fedora/linux'],
['IE', 'Esat Net', 'http://ftp.esat.net/mirrors/download.fedora.redhat.com/pub/fedora/linux'],
['IL', 'isoc-il', 'http://mirror.isoc.org.il/pub/fedora'],
['IN', 'IIT Kanpur', 'http://mirror.cse.iitk.ac.in/fedora'],
['IN', 'hnsfedoramirror', 'http://fedoramirror.hnsdc.com'],
['IN', 'GLUG-NITH', 'ftp://fedora.glug-nith.org/linux'],
['IS', 'RHnet', 'http://ftp.rhnet.is/pub/fedora/linux'],
['IS', 'Siminn', 'http://www.fedora.is/fedora'],
['IS', 'Skyggnir', 'http://fedora.skyggnir.is/linux'],
['IT', 'GARRMIRROR', 'http://fedora.mirror.garr.it/mirrors/fedora/linux'],
['IT', 'fedora.fastbull.org', 'http://fedora.fastbull.org/linux'],
['JP', 'RIKEN', 'http://ftp.riken.jp/Linux/fedora'],
['JP', 'JAIST', 'http://ftp.jaist.ac.jp/pub/Linux/Fedora'],
['JP', 'Internet Initiative Japan Inc.', 'http://ftp.iij.ad.jp/pub/linux/fedora'],
['JP', 'Dream Train Internet', 'http://ftp.dti.ad.jp/pub/Linux/Fedora'],
['JP', 'KDDI R&amp;D Laboratories Inc.', 'http://ftp.kddilabs.jp/Linux/packages/fedora'],
['JP', 'Yamagata University', 'http://ftp.yz.yamagata-u.ac.jp/pub/linux/fedora/linux'],
['KR', 'KAIST File Archive', 'http://ftp.kaist.ac.kr/fedora/linux'],
['LV', 'LU Linux Centrs', 'http://mirrors.linux.edu.lv/ftp.redhat.com/pub/fedora/linux'],
['MD', 'FedoraMD.org', 'http://repo.fedoramd.org/fedora/linux'],
['MX', 'UNAM Instituto de Fisiologia Celular', 'http://fedora.ifc.unam.mx'],
['MX', 'Facultad de Ingenieria, DIE, UNAM', 'ftp://ftp.fi-b.unam.mx/fedora/linux'],
['MY', 'OSCC MAMPU Malaysia Mirror', 'http://mirror.oscc.org.my/fedora'],
['NL', 'Leaseweb', 'http://mirror.leaseweb.com/fedora/linux'],
['NL', 'Delft University of Technology', 'http://ftp.tudelft.nl/download.fedora.redhat.com/linux'],
['NL', 'mirrors.kernel.org', 'http://mirrors.nl.eu.kernel.org/fedora'],
['NL', 'NLUUG-SURFnet', 'http://ftp.nluug.nl/pub/os/Linux/distr/fedora/linux'],
['NL', 'alviss', 'ftp://alviss.et.tudelft.nl/pub/fedora/linux'],
['NO', 'fedora.uib.no', 'http://fedora.uib.no/fedora/linux'],
['NZ', 'University of Canterbury', 'http://ucmirror.canterbury.ac.nz/linux/fedora/linux'],
['NZ', 'ftp.wicks.co.nz', 'http://ftp.wicks.co.nz/pub/linux/dist/fedora'],
['PL', 'ftp.man.poznan.pl', 'http://ftp.man.poznan.pl/pub/linux/fedora'],
['PL', 'ICM UW', 'http://ftp.icm.edu.pl/pub/Linux/fedora/linux'],
['PL', 'WCSS', 'http://ftp.wcss.pl/pub/linux/fedora/linux'],
['PL', 'Szczecin University of Technology', 'http://ftp.ps.pl/pub/Linux/fedora-linux'],
['PL', 'RPM Search FTP', 'ftp://ftp.pbone.net/pub/fedora/linux'],
['PT', 'ftp.up.pt', 'http://ftp.up.pt/fedora'],
['PT', 'DEI-FCT-UC', 'http://ftp.dei.uc.pt/pub/linux/fedora'],
['RO', 'RoEduNet Online Archive', 'http://ftp.roedu.net/mirrors/fedora.redhat.com/linux'],
['RO', 'RLUG', 'http://ftp.ines.lug.ro/fedora/linux'],
['RO', 'UPC Romania', 'http://ftp.astral.ro/mirrors/fedora/pub/fedora/linux'],
['RO', 'ArLUG', 'http://mirror.arlug.ro/pub/fedora/linux'],
['RO', 'RLUG', 'http://ftp.gts.lug.ro/fedora/linux'],
['RS', 'RC ETF Mirrors', 'http://mirror.etf.rs/fedora'],
['RU', 'Yandex', 'http://mirror.yandex.ru/fedora/linux'],
['RU', 'svk mirror', 'http://mirror.svk.su/fedora/linux'],
['RU', 'ftp.chg.ru', 'http://ftp.chg.ru/pub/Linux/fedora/linux'],
['RU', 'Inventa', 'http://ftp.rhd.ru/pub/fedora/linux'],
['SA', 'Internet Services Unit', 'http://mirrors.isu.net.sa/pub/fedora/linux'],
['SE', 'ftp.sunet.se', 'ftp://ftp.sunet.se/pub/Linux/distributions/fedora/linux'],
['SE', 'DF', 'http://ftp.df.lth.se/pub/fedora/linux'],
['SE', 'mirrors.kernel.org', 'http://mirrors.se.eu.kernel.org/fedora'],
['SG', 'ezNetworking Solutions Pte. Ltd.', 'ftp://ftp.oss.eznetsols.org/linux/fedora'],
['SG', 'National University of Singapore', 'http://mirror.nus.edu.sg/fedora'],
['SK', 'ftp.upjs.sk', 'http://ftp.upjs.sk/pub/fedora/linux'],
['TH', 'ISSP', 'http://mirrors.issp.co.th/fedora'],
['TR', 'LKD - linux.org.tr', 'http://ftp.linux.org.tr/fedora'],
['TR', 'Istanbul Technical University', 'http://ftp.itu.edu.tr/Mirror/Fedora/linux'],
['TR', 'Izmir Yuksek Teknoloji Enstitusu', 'http://linus.iyte.edu.tr/linux/fedora/linux'],
['TW', 'Shu-Te University', 'http://ftp.stu.edu.tw/Linux/Fedora/linux'],
['TW', 'I-Shou University', 'http://ftp.isu.edu.tw/pub/Linux/Fedora/linux'],
['TW', 'ftp.cse.yzu.edu.tw', 'ftp://ftp.cse.yzu.edu.tw/pub/Linux/Fedora'],
['TW', 'National Chi Nan University', 'http://ftp.ncnu.edu.tw/Linux/Fedora/linux'],
['UA', 'fedora.vc.ukrtel.net', 'http://fedora.vc.ukrtel.net/linux'],
['UA', 'ColoCall IDC Mirror Site', 'http://ftp.colocall.net/pub/fedora/linux'],
['UA', 'ABN', 'http://ftp.tlk-l.net/pub/mirrors/fedora'],
['US', 'FastSoft Mirror', 'http://chi-10g-1-mirror.fastsoft.net/pub/linux/fedora/linux'],
['US', 'mirrors.kernel.org', 'http://mirrors.kernel.org/fedora'],
['US', 'FastSoft Mirror', 'http://fedora.fastsoft.net/pub/linux/fedora/linux'],
['US', 'mirrors.secsup.org', 'http://fedora.secsup.org/linux'],
['US', 'mirrordenver.fdcservers.net', 'http://mirrordenver.fdcservers.net/fedora'],
['US', 'Reflected Networks', 'http://mirrors.reflected.net/fedora/linux'],
['US', 'FDCServers.net Chicago', 'http://mirror.fdcservers.net/fedora'],
['US', 'virginia.edu', 'http://nas1.itc.virginia.edu/fedora'],
['US', 'Astromirror', 'http://astromirror.uchicago.edu/fedora/linux'],
['US', 'mirror.us.as6453.net', 'http://mirror.us.as6453.net/fedora/linux'],
['US', 'mirror.yellowfiber.net', 'http://mirror.yellowfiber.net/fedora'],
['US', 'XMission Internet', 'http://mirrors.xmission.com/fedora'],
['US', 'Steadfast Networks', 'http://mirror.steadfast.net/fedora'],
['US', 'Argonne National Laboratory Public Software Mirror', 'http://mirror.anl.gov/pub/fedora/linux'],
['US', 'Indiana University', 'http://ftp.ussg.iu.edu/linux/fedora/linux'],
['US', 'University of Oregon', 'http://mirror.uoregon.edu/fedora/linux'],
['US', 'linux.nssl.noaa.gov', 'http://linux.nssl.noaa.gov/fedora/linux'],
['US', 'TDS', 'http://fedora.mirrors.tds.net/pub/fedora'],
['US', 'Rochester Institute of Technology', 'http://mirrors.rit.edu/fedora/linux'],
['US', 'University of Idaho', 'http://mirror.its.uidaho.edu/pub/fedora/linux'],
['US', 'Georgia Tech. Linux Mirror', 'http://www.gtlib.gatech.edu/pub/fedora.redhat/linux'],
['US', 'Canby Telcom', 'http://mirror.web-ster.com/fedora'],
['US', 'University of South Florida', 'http://ftp.usf.edu/pub/fedora/linux'],
['US', 'Oregon State University Open Source Lab', 'http://fedora.osuosl.org/linux'],
['US', 'University of Nebraska Lincoln', 'http://kdeforge.unl.edu/mirrors/fedora/linux'],
['US', 'University of Nebraska Lincoln', 'http://mirror.unl.edu/fedora/linux'],
['US', 'Applios', 'ftp://ftp.applios.net/pub/fedora/linux'],
['US', 'ftp.software.umn.edu', 'ftp://ftp.software.umn.edu/linux/fedora'],
['US', 'Fedora Server Beach', 'http://serverbeach1.fedoraproject.org/pub/fedora/linux'],
['US', 'mirror_vcu_edu', 'http://mirror.vcu.edu/pub/gnu+linux/fedora'],
['US', 'U. of Maryland', 'http://mirror.umoss.org/fedora/linux'],
['US', 'Utah State University', 'http://mirrors.usu.edu/fedora/linux'],
['US', 'Pavlov Media ', 'http://mirrors.pavlovmedia.net/fedora'],
['US', 'Linux@Duke', 'http://archive.linux.duke.edu/pub/fedora/linux'],
['US', 'Liberty University', 'http://mirror.liberty.edu/pub/fedora/linux'],
['US', 'Harvey Mudd College', 'http://mirror.hmc.edu/fedora/linux'],
['US', 'PenTeleData', 'http://mirrors.ptd.net/fedora/linux'],
['US', 'Princeton University CS', 'ftp://mirror.cs.princeton.edu/pub/mirrors/fedora/linux'],
['US', 'cse.buffalo.edu', 'ftp://ftp.cse.buffalo.edu/pub/Linux/fedora/linux'],
['US', 'New York Internet', 'ftp://mirror.nyi.net/fedora/linux'],
['US', 'NC State University', 'http://ftp.linux.ncsu.edu/pub/fedora/linux'],
['US', 'mirror.stanford.edu', 'http://mirror.stanford.edu/fedora/linux'],
['US', 'Virginia Tech', 'http://mirror.cc.vt.edu/pub/fedora/linux'],
['US', 'Portland State University', 'http://mirrors.cat.pdx.edu/fedora/linux'],
['US', 'mirrors.happyjacksoftware.com', 'http://mirrors.happyjacksoftware.com'],
['US', 'ftp.ndlug.nd.edu', 'http://ftp.ndlug.nd.edu/pub/fedora/linux'],
['US', 'cogentco.com', 'http://mirror.cogentco.com/pub/linux/fedora/linux'],
['US', 'tummy.com', 'http://mirrors.tummy.com/pub/fedora.redhat.com/fedora/linux'],
['US', 'UC Davis Library', 'http://mirror.lib.ucdavis.edu/fedora/linux'],
['US', 'HiWAAY', 'http://mirror.hiwaay.net/pub/fedora/linux'],
['US', 'distro.ibiblio.org', 'http://distro.ibiblio.org/pub/linux/distributions/fedora/linux'],
['US', 'Clarkson University', 'http://mirror.clarkson.edu/fedora/linux'],
['US', 'Newnan Utilities', 'http://mirror.newnanutilities.org/pub/fedora/linux'],
['US', 'The University of Texas at Austin', 'http://mirror.utexas.edu/fedora/linux'],
['US', 'DMACC', 'http://mirrors.dmacc.net/pub/fedora/linux'],
['US', 'WWU Mirror', 'ftp://ftp.wallawalla.edu/pub/mirrors/fedora/linux'],
['US', 'Nuvio Corporation', 'http://mirror.nuvio.com/pub/fedora/linux'],
]
    
def __set2():
    return [
['CN', 'Shanghai Jiao Tong University', 'ftp://ftp.sjtu.edu.cn/fedora/linux'],
]
    
__country_codes = {
"AX":"Aaland Islands",
"AF":"Afghanistan",
"AL":"Albania",
"DZ":"Algeria",
"AS":"American Samoa",
"AD":"Andorra",
"AO":"Angola",
"AI":"Anguilla",
"AQ":"Antarctica",
"AG":"Antigua And Barbuda",
"AR":"Argentina",
"AM":"Armenia",
"AW":"Aruba",
"AU":"Australia",
"AT":"Austria",
"AZ":"Azerbaijan",
"BS":"Bahamas",
"BH":"Bahrain",
"BD":"Bangladesh",
"BB":"Barbados",
"BY":"Belarus",
"BE":"Belgium",
"BZ":"Belize",
"BJ":"Benin",
"BM":"Bermuda",
"BT":"Bhutan",
"BO":"Bolivia",
"BA":"Bosnia And Herzegowina",
"BW":"Botswana",
"BV":"Bouvet Island",
"BR":"Brazil",
"IO":"British Indian Ocean Territory",
"BN":"Brunei Darussalam",
"BG":"Bulgaria",
"BF":"Burkina Faso",
"BI":"Burundi",
"KH":"Cambodia",
"CM":"Cameroon",
"CA":"Canada",
"CV":"Cape Verde",
"KY":"Cayman Islands",
"CF":"Central African Republic",
"TD":"Chad",
"CL":"Chile",
"CN":"China",
"CX":"Christmas Island",
"CC":"Cocos (Keeling) Islands",
"CO":"Colombia",
"KM":"Comoros",
"CD":"Congo, Democratic Republic Of (Was Zaire)",
"CG":"Congo, Republic Of",
"CK":"Cook Islands",
"CR":"Costa Rica",
"CI":"Cote D'Ivoire",
"HR":"Croatia (Local Name: Hrvatska)",
"CU":"Cuba",
"CY":"Cyprus",
"CZ":"Czech Republic",
"DK":"Denmark",
"DJ":"Djibouti",
"DM":"Dominica",
"DO":"Dominican Republic",
"EC":"Ecuador",
"EG":"Egypt",
"SV":"El Salvador",
"GQ":"Equatorial Guinea",
"ER":"Eritrea",
"EE":"Estonia",
"ET":"Ethiopia",
"FK":"Falkland Islands (Malvinas)",
"FO":"Faroe Islands",
"FJ":"Fiji",
"FI":"Finland",
"FR":"France",
"GF":"French Guiana",
"PF":"French Polynesia",
"TF":"French Southern Territories",
"GA":"Gabon",
"GM":"Gambia",
"GE":"Georgia",
"DE":"Germany",
"GH":"Ghana",
"GI":"Gibraltar",
"GR":"Greece",
"GL":"Greenland",
"GD":"Grenada",
"GP":"Guadeloupe",
"GU":"Guam",
"GT":"Guatemala",
"GN":"Guinea",
"GW":"Guinea-Bissau",
"GY":"Guyana",
"HT":"Haiti",
"HM":"Heard And Mc Donald Islands",
"HN":"Honduras",
"HK":"Hong Kong",
"HU":"Hungary",
"IS":"Iceland",
"IN":"India",
"ID":"Indonesia",
"IR":"Iran (Islamic Republic Of)",
"IQ":"Iraq",
"IE":"Ireland",
"IL":"Israel",
"IT":"Italy",
"JM":"Jamaica",
"JP":"Japan",
"JO":"Jordan",
"KZ":"Kazakhstan",
"KE":"Kenya",
"KI":"Kiribati",
"KP":"Korea, Democratic People'S Republic Of",
"KR":"Korea, Republic Of",
"KW":"Kuwait",
"KG":"Kyrgyzstan",
"LA":"Lao People'S Democratic Republic",
"LV":"Latvia",
"LB":"Lebanon",
"LS":"Lesotho",
"LR":"Liberia",
"LY":"Libyan Arab Jamahiriya",
"LI":"Liechtenstein",
"LT":"Lithuania",
"LU":"Luxembourg",
"MO":"Macau",
"MK":"Macedonia, The Former Yugoslav Republic Of",
"MG":"Madagascar",
"MW":"Malawi",
"MY":"Malaysia",
"MV":"Maldives",
"ML":"Mali",
"MT":"Malta",
"MH":"Marshall Islands",
"MQ":"Martinique",
"MR":"Mauritania",
"MU":"Mauritius",
"YT":"Mayotte",
"MX":"Mexico",
"FM":"Micronesia, Federated States Of",
"MD":"Moldova, Republic Of",
"MC":"Monaco",
"MN":"Mongolia",
"MS":"Montserrat",
"MA":"Morocco",
"MZ":"Mozambique",
"MM":"Myanmar",
"NA":"Namibia",
"NR":"Nauru",
"NP":"Nepal",
"NL":"Netherlands",
"AN":"Netherlands Antilles",
"NC":"New Caledonia",
"NZ":"New Zealand",
"NI":"Nicaragua",
"NE":"Niger",
"NG":"Nigeria",
"NU":"Niue",
"NF":"Norfolk Island",
"MP":"Northern Mariana Islands",
"NO":"Norway",
"OM":"Oman",
"PK":"Pakistan",
"PW":"Palau",
"PS":"Palestinian Territory, Occupied",
"PA":"Panama",
"PG":"Papua New Guinea",
"PY":"Paraguay",
"PE":"Peru",
"PH":"Philippines",
"PN":"Pitcairn",
"PL":"Poland",
"PT":"Portugal",
"PR":"Puerto Rico",
"QA":"Qatar",
"RE":"Reunion",
"RO":"Romania",
"RU":"Russian Federation",
"RW":"Rwanda",
"SH":"Saint Helena",
"KN":"Saint Kitts And Nevis",
"LC":"Saint Lucia",
"PM":"Saint Pierre And Miquelon",
"VC":"Saint Vincent And The Grenadines",
"WS":"Samoa",
"SM":"San Marino",
"ST":"Sao Tome And Principe",
"SA":"Saudi Arabia",
"SN":"Senegal",
"CS":"Serbia And Montenegro",
"SC":"Seychelles",
"SL":"Sierra Leone",
"SG":"Singapore",
"SK":"Slovakia",
"SI":"Slovenia",
"SB":"Solomon Islands",
"SO":"Somalia",
"ZA":"South Africa",
"GS":"South Georgia And The South Sandwich Islands",
"ES":"Spain",
"LK":"Sri Lanka",
"SD":"Sudan",
"SR":"Suriname",
"SJ":"Svalbard And Jan Mayen Islands",
"SZ":"Swaziland",
"SE":"Sweden",
"CH":"Switzerland",
"SY":"Syrian Arab Republic",
"TW":"Taiwan",
"TJ":"Tajikistan",
"TZ":"Tanzania, United Republic Of",
"TH":"Thailand",
"TL":"Timor-Leste",
"TG":"Togo",
"TK":"Tokelau",
"TO":"Tonga",
"TT":"Trinidad And Tobago",
"TN":"Tunisia",
"TR":"Turkey",
"TM":"Turkmenistan",
"TC":"Turks And Caicos Islands",
"TV":"Tuvalu",
"UG":"Uganda",
"UA":"Ukraine",
"AE":"United Arab Emirates",
"GB":"United Kingdom",
"US":"United States",
"UM":"United States Minor Outlying Islands",
"UY":"Uruguay",
"UZ":"Uzbekistan",
"VU":"Vanuatu",
"VA":"Vatican City State (Holy See)",
"VE":"Venezuela",
"VN":"Viet Nam",
"VG":"Virgin Islands (British)",
"VI":"Virgin Islands (U.S.)",
"WF":"Wallis And Futuna Islands",
"EH":"Western Sahara",
"YE":"Yemen",
"ZM":"Zambia",
"ZW":"Zimbabwe",
}

def all_candidate_repositories():
    ret = __set1() + __set2()
    for e in ret:
        assert len(e) == 3
        try:
            e[0] = __country_codes[e[0]]
        except KeyError:
            pass
        assert not e[2].endswith('/')
        
    return ret

class FedoraReposSection:
    def __init__(self, lines):
        for line in lines: assert isinstance(line, str) and line.endswith('\n')
        assert lines[0].startswith('['), lines
        
        self.lines = lines

    def is_fedora_repos(self):
        for line in self.lines:
            if line.startswith('gpgkey=') and 'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$basearch' in line:
                return True
        return False

    def part2_of(self, line):
        for word in ['/releases/', '/development/', '/updates/']:
            pos = line.find(word)
            if pos != -1:
                return line[pos:]
        else:
            raise CommandFailError('No /releases/, /development/ or /updates/ found.', self.lines)

    def comment_line(self, i):
        if not self.lines[i].startswith('#'):
            self.lines[i] = '#' + self.lines[i] 

    def uncomment_line(self, i):
        if self.lines[i].startswith('#'):
            self.lines[i] = self.lines[i][1:] 

    def change_baseurl(self, new_url):
        for i, line in enumerate(self.lines):
            if 'mirrorlist=' in line:
                self.comment_line(i)
            elif 'baseurl=' in line:
                self.uncomment_line(i)
        for i, line in enumerate(self.lines):
            if line.startswith('baseurl='):
                self.lines[i] = 'baseurl=' + new_url + self.part2_of(line)

    def write_to_stream(self, stream):
        stream.writelines(self.lines)
    
    def enabled(self):
        return 'enabled=1\n' in self.lines

class FedoraReposFile:
    def __init__(self, path):
        assert isinstance(path, str) and path.endswith('.repo')

        self.path = path

        self.sections = []
        with open(path) as f:
            contents = f.readlines()
        while contents[0].startswith('#') or contents[0].strip() == '': # skip comments and blank lines at the beginning
            del contents[0]
        lines = []
        for line in contents:
            if line.startswith('[') and lines:
                section = FedoraReposSection(lines)
                self.sections.append(section)
                lines = []
            lines.append(line)
        section = FedoraReposSection(lines)
        self.sections.append(section)

    def change_baseurl(self, new_url):
        changed = False
        for section in self.sections:
            if section.is_fedora_repos():
                section.change_baseurl(new_url)
                changed = True

        if not changed: return
        with TempOwn(self.path) as o:
            with open(self.path, 'w') as f:
                for section in self.sections:
                    section.write_to_stream(f)

    @classmethod
    def all_repo_paths(cls):
        import glob
        return glob.glob('/etc/yum.repos.d/*.repo')

    @classmethod
    def all_repo_objects(cls):
        ret = []
        for path in cls.all_repo_paths():
            obj = FedoraReposFile(path)
            ret.append(obj)
        return ret
