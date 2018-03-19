# -*- coding: UTF-8 -*-
from setuphelpers import *

uninstallkey = []

def install():

    if windows_version() < Version('6.1'):
        error("Firefox >= 53 n'est plus disponible pour XP")
    version = control.version.split('-',1)[0]
    ukey = 'Mozilla Firefox %s (x86 fr)'%version
    exe = 'Firefox Setup %s.exe'%version
    install_exe_if_needed(exe,'-ms',key=ukey,min_version=version,killbefore='firefox.exe')


def update_package():
    """updates the package / control version with the latest stable firefox version"""
    import re,requests,urlparse,glob

    # get index of all dowloads
    """
    #url_base = 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/latest/win32/fr/'
    url_base = 'https://download-installer.cdn.mozilla.net/pub/firefox/releases/43.0/win32/fr/'
    index = wgets(url_base)

    # get list of lastest french versions
    re_setup = re.compile(r'<a href=".*/(Firefox%20Setup%20[0-9.]*.exe)">Firefox Setup .*</a>')
    filename = urlparse.unquote(re_setup.findall(index)[0])
    url = url_base+filename
    """
    url = requests.head('https://download.mozilla.org/?product=firefox-latest&os=win&lang=fr').headers['Location']
    filename = urlparse.unquote(url.rsplit('/',1)[1])

    if not isfile(filename):
        print('Downloading %s from %s'%(filename,url))
        wget(url,filename)

    # removes old exe
    if isfile(filename):
        exes = glob.glob('Firefox*.exe')
        for fn in exes:
            if fn != filename:
                remove_file(fn)

        # updates control version from filename, increment package version.
        control = PackageEntry().load_control_from_wapt ('.')
        control.version = '%s-%s'%(re.findall('Firefox Setup (.*)\.exe',filename)[0],int(control.version.split('-',1)[1])+1)
        control.save_control_to_wapt('.')


if __name__ == '__main__':
    update_package()
