# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.
#

from setuptools import setup, find_packages
from os import listdir, system


langs = []
for l in listdir('languages'):
    if l.endswith('ts'):
        system('lrelease-qt5 languages/%s' % l)
        langs.append(('languages/%s' % l).replace('.ts', '.qm'))


system('pyrcc5 kaptan.qrc -o kaptan5/rc_kaptan.py')

datas = [('/usr/share/applications', ['data/kaptan.desktop']),
         ('/etc/skel/.config/autostart', ['data/kaptan.desktop']),
         ('/usr/share/icons/hicolor/64x64/apps', ['data/images/kaptan.svg']),
         ('/usr/share/kaptan/languages', langs)]

setup(
    name = "kaptan",
    scripts = ["script/kaptan"],
    packages = find_packages(),
    version = "5.0",
    license = "GPL v3",
    description = "KaoS desktop configurate.",
    author = "Metehan Özbek, Anke Boermsa",
    author_email = "mthnzbk@gmail.com, demm@kaosx.us",
    url = "https://github.com/KaOSx/kaptan",
    keywords = ["PyQt5"],
    data_files = datas
)

