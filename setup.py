from setuptools import setup

config = {
    'description': 'AddressBook 1.0 - simple contact manager',
    'author': 'Anna Brzozowska',
    'url': '',
    'author_email': 'brzozowskaanna5@gmail.com',
    'version': '1.0',
    'install_requires': [],
    'packages': ['addressbook', 'addressbook.ab_windows'],
    'scripts': [],
    'name': 'AddressBook'
}

setup(**config)