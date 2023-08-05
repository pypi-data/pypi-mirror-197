# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_admin',
 'flask_admin.contrib',
 'flask_admin.contrib.appengine',
 'flask_admin.contrib.fileadmin',
 'flask_admin.contrib.geoa',
 'flask_admin.contrib.mongoengine',
 'flask_admin.contrib.peewee',
 'flask_admin.contrib.peeweemodel',
 'flask_admin.contrib.pymongo',
 'flask_admin.contrib.sqla',
 'flask_admin.contrib.sqlamodel',
 'flask_admin.form',
 'flask_admin.model',
 'flask_admin.tests',
 'flask_admin.tests.fileadmin',
 'flask_admin.tests.geoa',
 'flask_admin.tests.mongoengine',
 'flask_admin.tests.peeweemodel',
 'flask_admin.tests.pymongo',
 'flask_admin.tests.sqla',
 'flask_admin.translations']

package_data = \
{'': ['*'],
 'flask_admin': ['static/admin/css/bootstrap2/*',
                 'static/admin/css/bootstrap3/*',
                 'static/admin/css/bootstrap4/*',
                 'static/admin/js/*',
                 'static/bootstrap/bootstrap2/css/*',
                 'static/bootstrap/bootstrap2/js/*',
                 'static/bootstrap/bootstrap2/swatch/amelia/*',
                 'static/bootstrap/bootstrap2/swatch/cerulean/*',
                 'static/bootstrap/bootstrap2/swatch/cosmo/*',
                 'static/bootstrap/bootstrap2/swatch/cyborg/*',
                 'static/bootstrap/bootstrap2/swatch/default/*',
                 'static/bootstrap/bootstrap2/swatch/flatly/*',
                 'static/bootstrap/bootstrap2/swatch/img/*',
                 'static/bootstrap/bootstrap2/swatch/journal/*',
                 'static/bootstrap/bootstrap2/swatch/readable/*',
                 'static/bootstrap/bootstrap2/swatch/simplex/*',
                 'static/bootstrap/bootstrap2/swatch/slate/*',
                 'static/bootstrap/bootstrap2/swatch/spacelab/*',
                 'static/bootstrap/bootstrap2/swatch/spruce/*',
                 'static/bootstrap/bootstrap2/swatch/superhero/*',
                 'static/bootstrap/bootstrap2/swatch/united/*',
                 'static/bootstrap/bootstrap3/css/*',
                 'static/bootstrap/bootstrap3/js/*',
                 'static/bootstrap/bootstrap3/swatch/cerulean/*',
                 'static/bootstrap/bootstrap3/swatch/cosmo/*',
                 'static/bootstrap/bootstrap3/swatch/cyborg/*',
                 'static/bootstrap/bootstrap3/swatch/darkly/*',
                 'static/bootstrap/bootstrap3/swatch/default/*',
                 'static/bootstrap/bootstrap3/swatch/flatly/*',
                 'static/bootstrap/bootstrap3/swatch/fonts/*',
                 'static/bootstrap/bootstrap3/swatch/journal/*',
                 'static/bootstrap/bootstrap3/swatch/lumen/*',
                 'static/bootstrap/bootstrap3/swatch/paper/*',
                 'static/bootstrap/bootstrap3/swatch/readable/*',
                 'static/bootstrap/bootstrap3/swatch/sandstone/*',
                 'static/bootstrap/bootstrap3/swatch/simplex/*',
                 'static/bootstrap/bootstrap3/swatch/slate/*',
                 'static/bootstrap/bootstrap3/swatch/spacelab/*',
                 'static/bootstrap/bootstrap3/swatch/superhero/*',
                 'static/bootstrap/bootstrap3/swatch/united/*',
                 'static/bootstrap/bootstrap3/swatch/yeti/*',
                 'static/bootstrap/bootstrap4/*',
                 'static/bootstrap/bootstrap4/css/*',
                 'static/bootstrap/bootstrap4/fonts/*',
                 'static/bootstrap/bootstrap4/js/*',
                 'static/bootstrap/bootstrap4/swatch/cerulean/*',
                 'static/bootstrap/bootstrap4/swatch/cosmo/*',
                 'static/bootstrap/bootstrap4/swatch/cyborg/*',
                 'static/bootstrap/bootstrap4/swatch/darkly/*',
                 'static/bootstrap/bootstrap4/swatch/default/*',
                 'static/bootstrap/bootstrap4/swatch/flatly/*',
                 'static/bootstrap/bootstrap4/swatch/journal/*',
                 'static/bootstrap/bootstrap4/swatch/litera/*',
                 'static/bootstrap/bootstrap4/swatch/lumen/*',
                 'static/bootstrap/bootstrap4/swatch/lux/*',
                 'static/bootstrap/bootstrap4/swatch/materia/*',
                 'static/bootstrap/bootstrap4/swatch/minty/*',
                 'static/bootstrap/bootstrap4/swatch/pulse/*',
                 'static/bootstrap/bootstrap4/swatch/sandstone/*',
                 'static/bootstrap/bootstrap4/swatch/simplex/*',
                 'static/bootstrap/bootstrap4/swatch/sketchy/*',
                 'static/bootstrap/bootstrap4/swatch/slate/*',
                 'static/bootstrap/bootstrap4/swatch/solar/*',
                 'static/bootstrap/bootstrap4/swatch/spacelab/*',
                 'static/bootstrap/bootstrap4/swatch/superhero/*',
                 'static/bootstrap/bootstrap4/swatch/united/*',
                 'static/bootstrap/bootstrap4/swatch/yeti/*',
                 'static/vendor/*',
                 'static/vendor/bootstrap-daterangepicker/*',
                 'static/vendor/bootstrap4/*',
                 'static/vendor/fontawesome-free-5.1.0-web/css/*',
                 'static/vendor/fontawesome-free-5.1.0-web/js/*',
                 'static/vendor/fontawesome-free-5.1.0-web/less/*',
                 'static/vendor/fontawesome-free-5.1.0-web/metadata/*',
                 'static/vendor/fontawesome-free-5.1.0-web/scss/*',
                 'static/vendor/fontawesome-free-5.1.0-web/sprites/*',
                 'static/vendor/fontawesome-free-5.1.0-web/svgs/brands/*',
                 'static/vendor/fontawesome-free-5.1.0-web/svgs/regular/*',
                 'static/vendor/fontawesome-free-5.1.0-web/svgs/solid/*',
                 'static/vendor/fontawesome-free-5.1.0-web/webfonts/*',
                 'static/vendor/leaflet/*',
                 'static/vendor/leaflet/images/*',
                 'static/vendor/multi-level-dropdowns-bootstrap/*',
                 'static/vendor/select2/*',
                 'static/vendor/x-editable/css/*',
                 'static/vendor/x-editable/img/*',
                 'static/vendor/x-editable/js/*',
                 'templates/bootstrap2/admin/*',
                 'templates/bootstrap2/admin/file/*',
                 'templates/bootstrap2/admin/file/modals/*',
                 'templates/bootstrap2/admin/model/*',
                 'templates/bootstrap2/admin/model/modals/*',
                 'templates/bootstrap2/admin/rediscli/*',
                 'templates/bootstrap3/admin/*',
                 'templates/bootstrap3/admin/file/*',
                 'templates/bootstrap3/admin/file/modals/*',
                 'templates/bootstrap3/admin/model/*',
                 'templates/bootstrap3/admin/model/modals/*',
                 'templates/bootstrap3/admin/rediscli/*',
                 'templates/bootstrap4/admin/*',
                 'templates/bootstrap4/admin/file/*',
                 'templates/bootstrap4/admin/file/modals/*',
                 'templates/bootstrap4/admin/model/*',
                 'templates/bootstrap4/admin/model/modals/*',
                 'templates/bootstrap4/admin/rediscli/*'],
 'flask_admin.tests': ['data/*',
                       'fileadmin/files/*',
                       'sqla/templates/*',
                       'templates/*',
                       'tmp/*',
                       'tmp/inner/*'],
 'flask_admin.translations': ['af/LC_MESSAGES/*',
                              'ar/LC_MESSAGES/*',
                              'be/LC_MESSAGES/*',
                              'ca_ES/LC_MESSAGES/*',
                              'cs/LC_MESSAGES/*',
                              'da/LC_MESSAGES/*',
                              'de/LC_MESSAGES/*',
                              'el/LC_MESSAGES/*',
                              'en/LC_MESSAGES/*',
                              'es/LC_MESSAGES/*',
                              'et/LC_MESSAGES/*',
                              'fa/LC_MESSAGES/*',
                              'fi/LC_MESSAGES/*',
                              'fr/LC_MESSAGES/*',
                              'he/LC_MESSAGES/*',
                              'hu/LC_MESSAGES/*',
                              'it/LC_MESSAGES/*',
                              'ja/LC_MESSAGES/*',
                              'ko/LC_MESSAGES/*',
                              'nl/LC_MESSAGES/*',
                              'no/LC_MESSAGES/*',
                              'pa/LC_MESSAGES/*',
                              'pl/LC_MESSAGES/*',
                              'pt/LC_MESSAGES/*',
                              'pt_BR/LC_MESSAGES/*',
                              'ro/LC_MESSAGES/*',
                              'ru/LC_MESSAGES/*',
                              'sk/LC_MESSAGES/*',
                              'sr/LC_MESSAGES/*',
                              'sv/LC_MESSAGES/*',
                              'tr/LC_MESSAGES/*',
                              'uk/LC_MESSAGES/*',
                              'vi/LC_MESSAGES/*',
                              'zh_Hans_CN/LC_MESSAGES/*',
                              'zh_Hant_TW/LC_MESSAGES/*']}

setup_kwargs = {
    'name': 'flask-admin-plus',
    'version': '1.6.16',
    'description': 'Flask Admin with a few more features and improvements',
    'long_description': 'None',
    'author': 'Sean McCarthy',
    'author_email': 'smccarthy@myijack.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
