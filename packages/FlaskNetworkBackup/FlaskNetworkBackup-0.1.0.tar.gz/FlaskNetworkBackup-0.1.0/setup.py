from setuptools import setup, find_packages
import os


install_dir = os.path.join(os.getcwd(), 'FlaskNetworkBackup')
os.environ['PATH'] += os.pathsep + install_dir

setup(
    name='FlaskNetworkBackup',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Flask', 'netmiko'],
    entry_points={
        'console_scripts': [
            'flask-netbackup  = FlaskNetworkBackup.NetBackup:main'
        ]
    },
    license='GPLv3',
    author='Diyar Bagis',
    author_email='diyarbagis@gmail.com',
    description='A free open-source Flask app for backup on switches,routers and firewalls.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/diyarbagis/FlaskNetworkBackup',
    keywords='flask network firewall switch router backup',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Networking :: Firewalls',
    ],
)


os.environ['PATH'] += os.pathsep + install_dir

