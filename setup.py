import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='netkeiba',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app which crawls and imports race data from netkeiba.com',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Hank Ehly',
    author_email='henry.ehly@gmail.com',
    url='https://github.com/hankehly/netkeiba',
    install_requires=[
        'scrapy>=1.6.0',
        'beautifulsoup4>=4.7.1',
        'python-dateutil>=2.8.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
