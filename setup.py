from setuptools import setup

config = {
    'description': 'Simple contact manager',
    'author': 'Anna Brzozowska',
    'url': '',
    'author_email': 'brzozowskaanna5@gmail.com',
    'version': '1.0',
    'install_requires': ['xlwt', ],
    'packages': ['addressbook', 'addressbook.ab_windows'],
    'scripts': [],
    'name': 'AddressBook',
    'keywords': ['addressbook', 'phonebook']
}

setup(**config, requires=['xlwt'])
