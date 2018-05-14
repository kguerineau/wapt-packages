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
from setuphelpers import *

uninstallkey = []

def install():
    print('installing tis-ccleaner')
    exes = glob.glob('*.exe')

    def vers_ccleaner(ukey):
        if iswin64():
            return get_file_properties(makepath(install_location(ukey['key']),"CCleaner64.exe"))['ProductVersion'].replace(', ','.')
        else:
            return get_file_properties(makepath(install_location(ukey['key']),"CCleaner.exe"))['ProductVersion'].replace(', ','.')

    install_exe_if_needed(exes[0] ,silentflags="/S",key="CCleaner",min_version=control['version'].split('-',1)[0],get_version=vers_ccleaner)

    print("Override settings")
    filecopyto("ccleaner.ini", makepath(install_location("CCleaner"),"ccleaner.ini"))
    #https://singularlabs.com/software/ccenhancer/download-ccenhancer/
    filecopyto("winapp2.ini", makepath(install_location("CCleaner"),"winapp2.ini"))

def session_setup():
    registry_set(HKEY_CURRENT_USER,'software\\Piriform\\CCleaner', 'Monitoring','0')
    registry_set(HKEY_CURRENT_USER,'software\\Piriform\\CCleaner', 'SystemMonitoring','0')
    registry_set(HKEY_CURRENT_USER,'software\\Piriform\\CCleaner', 'UpdateCheck','0')
    registry_set(HKEY_CURRENT_USER,'software\\Piriform\\CCleaner', 'RunICS','0')
    registry_set(HKEY_CURRENT_USER,'software\\Piriform\\CCleaner', 'CheckTrialOffer','0')

def update_package():

    import requests,BeautifulSoup
    page = requests.get('http://www.piriform.com/ccleaner/download/standard',headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}).text
    bs = BeautifulSoup.BeautifulSoup(page)
    download = bs.find(id="BigDownload").a["href"]
    filename = download.rsplit('/',1)[1]

    # on ne telecharge que si on ne l'a pas deja
    if not isfile(filename):
        wget(download, filename)
    else:
        print(u'Le setup %s est déjà présent dans le paquet.' % filename)

    # on enleve les vieux exes
    for fn in glob.glob('*.exe'):
        if fn != filename :
            print('Suppression du vieux exe %s'%fn)
            remove_file(fn)

    vers = get_file_properties(filename)['ProductVersion']
    os.chdir(os.path.dirname(__file__))
    from waptpackage import PackageEntry
    pe = PackageEntry()
    pe.load_control_from_wapt(os.getcwd())
    pe.version = vers + '-0'
    pe.save_control_to_wapt(os.getcwd())


if __name__ == '__main__':
    update_package()

