import distribute_setup
distribute_setup.use_setuptools()

import os
from setuptools import setup, find_packages
from synnefo.util.version import update_version

HERE = os.path.abspath(os.path.normpath(os.path.dirname(__file__)))
update_version('okeanos_site', 'version', HERE)
from okeanos_site.version import __version__


# Package info
VERSION = __version__
README = open(os.path.join(HERE, 'README')).read()
CHANGES = open(os.path.join(HERE, 'Changelog')).read()
SHORT_DESCRIPTION = 'Package short description'

PACKAGES_ROOT = '.'
PACKAGES = find_packages(PACKAGES_ROOT)

# Package meta
CLASSIFIERS = []

# Package requirements
INSTALL_REQUIRES = [
]

TESTS_REQUIRES = [
]

PACKAGE_DATA = {
    'okeanos_site': [
        'templates/okeanos/*.html',
        'templates/okeanos/pages/*.html',
        'static/okeanos_static/css/*.css',
        'static/okeanos_static/js/*.js',
        'static/okeanos_static/images/*.png',
        'static/okeanos_static/video/*.txt',
        'static/okeanos_static/video/*.js',
        'static/okeanos_static/video/*.css',
        'static/okeanos_static/video/skins/*.css',
    ]
}

setup(
    name = 'snf-okeanos-site',
    version = VERSION,
    license = 'BSD',
    url = 'http://code.grnet.gr/',
    description = SHORT_DESCRIPTION,
    long_description=README + '\n\n' +  CHANGES,
    classifiers = CLASSIFIERS,

    author = '~okeanos dev team - GRNET',
    author_email = 'okeanos-dev@lists.grnet.gr',
    maintainer = 'Kostas Papadimitriou',
    maintainer_email = 'kpap@grnet.gr',

    packages = PACKAGES,
    package_dir= {'': PACKAGES_ROOT},
    include_package_data = True,
    package_data = PACKAGE_DATA,
    zip_safe = False,

    entry_points = {
        'synnefo': [
            'default_settings = okeanos_site.settings',
            'web_apps = okeanos_site:synnefo_web_apps',
            'web_static = okeanos_site:synnefo_static_files',
            'urls = okeanos_site.urls:urlpatterns'
        ]
    },

    install_requires = INSTALL_REQUIRES,
)

