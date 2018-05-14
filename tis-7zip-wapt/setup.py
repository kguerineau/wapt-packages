#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
#    This file is part of WAPT
#    Copyright (C) 2013  Tranquil IT Systems http://www.tranquil.it
#    WAPT aims to help Windows systems administrators to deploy
#    setup and update applications on users PC.
#
#    WAPT is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WAPT is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WAPT.  If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------

import platform
import time
from setuphelpers import *

uninstallkey=[]

""" You can do a CTRL F9 in pyscripter to update the package """

def install():
    global uninstallkey
    from common import Wapt

    broken_7zip = [ soft for soft in installed_softwares('7-zip') if Version(soft['version']) < Version('16.0') ]
    if broken_7zip:
        for uninstall in broken_7zip:
            cmd = WAPT.uninstall_cmd(uninstall['key'])
            print(u'uninstalling %s' % (uninstall['name'],))
            # on execute la commande de desinstallation
            run(cmd)

    allmsi = glob.glob('*-x64.msi')
    for msi in allmsi:
        if iswin64():
            install_msi_if_needed(msi,killbefore=['7zFM.exe'])
        else:
            install_msi_if_needed(msi.replace('-x64.msi','.msi'),killbefore=['7zFM.exe'])

    for ext in ('.001','.7z','.arj','.bz2','.bzip2','.cab','.cpio','.deb','.dmg','.fat',
            '.gz','.gzip','.hfs','.iso','.lha','.lzh','.lzma','.ntfs','.rar','.rpm',
            '.squashfs','.swm','.tar','.taz','.tbz','.tbz2','.tgz','.tpz','.txz','.vhd',
            '.wim','.xar','.xz','.z','.zip', '.zipe'):
        register_ext('7-zip',ext,'"%s" "%%1"' % (makepath(programfiles,'7-zip','7zFM.exe'),),icon="%s,1" % (makepath(programfiles,'7-zip','7z.dll')))

""" You can do a CTRL F9 in pyscripter to update the package """









def update_sources():

    import urllib2
    import requests

    """I download the file >>>"""

    sock = urllib2.urlopen("http://www.7-zip.org/download.html",timeout=10)
    htmlSource = sock.readlines()
    sock.close()
    for line in htmlSource :
        if  'x64.msi'  in line :
            start = line.find('href=')
            end = line.find('">D')
            x64 = line[start + 6:end]
            x86 = x64.replace("-x64.msi",".msi")
            break

    allmsi = glob.glob('*.msi')
    for msi in allmsi:
        remove_file(msi)

    wget('http://www.7-zip.org/%s' % x64, x64.rsplit('/')[-1])
    wget('http://www.7-zip.org/%s' % x86, x86.rsplit('/')[-1])



    """I retrieve the current version from the msi """

    allmsi = glob.glob('*.msi')
    for msi in allmsi:
        vers = get_msi_properties(msi)['ProductVersion']
        break

    """I write the version in the control file >>>"""

    os.chdir(os.path.dirname(__file__))

    from waptpackage import PackageEntry
    pe = PackageEntry()
    pe.load_control_from_wapt(os.getcwd())

    pe.version = vers + '-0'
    pe.save_control_to_wapt(os.getcwd())


if __name__ == '__main__':
    update_sources()




