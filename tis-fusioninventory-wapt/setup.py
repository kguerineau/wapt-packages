# -*- coding: utf-8 -*-
from setuphelpers import *

uninstallkey = []


serveur = "http://glpi/glpi/plugins/fusioninventory/"

parameters = '/S /acceptlicense /server="%s" /execmode=service /no-ssl-check /runnow' % (serveur)

key='FusionInventory-Agent'

def install():

    print('installing Fusion inventory agent')
    versionpaquet = control['version'].split('-',1)[0]
    if iswin64():
        install_exe_if_needed("fusioninventory-agent_windows-x64_%s.exe" % versionpaquet,parameters,key=key,min_version=versionpaquet)
    else:
        install_exe_if_needed("fusioninventory-agent_windows-x86_%s.exe" % versionpaquet,parameters,key=key,min_version=versionpaquet)




def update_package():
    import BeautifulSoup,requests,re

    from waptpackage import PackageEntry
    verify=True
    pe = PackageEntry()
    pe.load_control_from_wapt(os.getcwd())
    current_version = pe['version'].split('-',1)[0]
    verify=True

    url = 'https://github.com/fusioninventory/fusioninventory-agent/releases'

    import requests,BeautifulSoup
    page = requests.get(url + '/latest',headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'},verify=verify).text
    bs = BeautifulSoup.BeautifulSoup(page)

    version = str(bs.find('a',{'class':'css-truncate'}).text)

    url64 = url + "/download/" + version + "/fusioninventory-agent_windows-x64_%s.exe" % version
    url86 = url + "/download/" + version + "/fusioninventory-agent_windows-x86_%s.exe" % version

    filenamex86 = "fusioninventory-agent_windows-x86_%s.exe" % version
    filenamex64 = "fusioninventory-agent_windows-x64_%s.exe" % version

    if not isfile( filenamex64 ) :
        wget( url64 )
    if not isfile( filenamex86 ) :
        wget( url86 )


    for fileexe in glob.glob('fusioninventory-agent_windows-x64*.exe'):
        if fileexe != filenamex64 :
            print('Delete ' + fileexe)
            remove_file(fileexe)

    for fileexe in glob.glob('fusioninventory-agent_windows-x86*.exe'):
        if fileexe != filenamex86 :
            print('Delete ' + fileexe)
            remove_file(fileexe)

    if not isfile(filenamex64):
        print('Download ' + url64)
        wget(url64,filenamex64)

    if not isfile(filenamex86):
        print('Download ' + url86)
        wget(url86,filenamex86)

    vers = get_file_properties(filenamex64)['ProductVersion']
    os.chdir(os.path.dirname(__file__))
    from waptpackage import PackageEntry
    pe = PackageEntry()
    pe.load_control_from_wapt(os.getcwd())
    pe.version = vers + '-0'
    pe.save_control_to_wapt(os.getcwd())


if __name__ == '__main__':
    update_package()

