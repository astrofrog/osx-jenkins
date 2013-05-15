import os
import shutil
import urllib2

DISTRIBUTE_VERSION = "0.6.40"
PIP_VERSION = "1.3.1"

PYTHON_URL = "http://www.python.org/ftp/python/{version}/Python-{version}.tar.{ext}"
DISTRIBUTE_URL = "https://pypi.python.org/packages/source/d/distribute/distribute-{dv}.tar.gz".format(dv=DISTRIBUTE_VERSION)
PIP_URL = "https://pypi.python.org/packages/source/p/pip/pip-{pv}.tar.gz".format(pv=PIP_VERSION)

def download(url):
    u = urllib2.urlopen(url)
    f = open(os.path.basename(url), 'wb')
    f.write(u.read())
    f.close()
    os.system('tar xvzf {filename}'.format(filename=os.path.basename(url)))


for version in ['2.6.8', '2.7.4', '3.1.5', '3.2.4', '3.3.1']:

    short_version = version[:3]

    if os.path.exists('Python-{version}'.format(version=version)):
        shutil.rmtree('Python-{version}'.format(version=version))

    download(PYTHON_URL.format(version=version, ext='xz' if version == '3.3.1' else 'gz'))
    
    os.chdir('Python-{version}'.format(version=version))    
    os.system('./configure --prefix=$HOME/usr/python ; make ; make install')
    os.chdir('..')

    shutil.rmtree('Python-{0:s}'.format(version))

    if os.path.exists('distribute-{dv}'.format(dv=DISTRIBUTE_VERSION)):
        shutil.rmtree('distribute-{dv}'.format(dv=DISTRIBUTE_VERSION))

    download(DISTRIBUTE_URL)

    os.chdir('distribute-{dv}'.format(dv=DISTRIBUTE_VERSION))
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('distribute-{dv}'.format(dv=DISTRIBUTE_VERSION))

    if os.path.exists('pip-{pipv}'.format(pipv=PIP_VERSION)):
        shutil.rmtree('pip-{pipv}'.format(pipv=PIP_VERSION))

    download(PIP_URL)

    os.chdir('pip-{pipv}'.format(pipv=PIP_VERSION))
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('pip-{pipv}'.format(pipv=PIP_VERSION))

    os.system('$HOME/usr/python/bin/pip-{0:s} install virtualenv'.format(short_version))

