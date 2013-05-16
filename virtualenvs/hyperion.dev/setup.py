import os
import sys
import urllib2
import subprocess
from copy import deepcopy
from distutils import version

NUMPY_VERSIONS = ['1.5.1', '1.6.2', '1.7.1']
PYTHON_VERSIONS = ['2.6', '2.7', '3.1', '3.2', '3.3']
H5PY_VERSIONS = ['1.3.1', '2.0.0', '2.0.1', '2.1.3']

NUMPY_URL = "https://pypi.python.org/packages/source/n/numpy/numpy-{nv}.tar.gz"
H5PY_URL = "https://h5py.googlecode.com/files/h5py-{hv}.tar.gz"

def download(url):
    print "Downloading " + url
    u = urllib2.urlopen(url)
    f = open(os.path.basename(url), 'wb')
    f.write(u.read())
    f.close()
    
for nv in NUMPY_VERSIONS:
    if not os.path.exists('numpy-{nv}.tar.gz'.format(nv=nv)):
        download(NUMPY_URL.format(nv=nv))

for hv in H5PY_VERSIONS:
    if not os.path.exists('h5py-{hv}.tar.gz'.format(hv=hv)):
        download(H5PY_URL.format(hv=hv))


SCRIPT = """
# Create virtual environment
$HOME/usr/python/bin/virtualenv-{pv} --python=$HOME/usr/python/bin/python{pv} --no-site-packages --distribute {full}

# Install Cython
# {full}/bin/pip-{pv} install Cython

# Unpack Numpy to temporary directory
mkdir {full}.tmp1
tar -C {full}.tmp1 -xvzf numpy-{nv}.tar.gz

# Change to directory
cd {full}.tmp1/numpy-{nv}/

# Build Numpy
# FFLAGS="-m64" ../{full}/bin/python{pv} setup.py build --fcompiler=gnu95'.format(**versions)
CC={cc} ../../{full}/bin/python{pv} setup.py build
../../{full}/bin/python{pv} setup.py install

# Back to start
cd ../../

# Remove temporary directory
rm -r {full}.tmp1

# Unpack h5py to temporary directory
mkdir {full}.tmp2
tar -C {full}.tmp2 -xvzf h5py-{hv}.tar.gz

# Change to directory
cd {full}.tmp2/h5py-{hv}/

# Build h5py
../../{full}/bin/python{pv} setup.py build --hdf5=$HOME/usr/hdf5-1.8.5
../../{full}/bin/python{pv} setup.py install

# Back to start
cd ../../

# Remove temporary directory
rm -r {full}.tmp2

# Install Astropy
{full}/bin/pip-{pv} install astropy
"""


def setup_virtualenv(versions):

    print versions['full']

    f = open('{full}.log'.format(**versions), 'wb')
    code = subprocess.call(SCRIPT.format(**versions), shell=True, stdout=f, stderr=f)
    f.close()

all_versions = []

versions = {}
for h5py_version in H5PY_VERSIONS:
    versions['hv'] = h5py_version
    for numpy_version in NUMPY_VERSIONS:
        versions['nv'] = numpy_version
        for python_version in PYTHON_VERSIONS:
            if python_version in ['3.3']:
                if version.LooseVersion(numpy_version) < version.LooseVersion("1.7.0"):
                    continue
            if version.LooseVersion(python_version) >= version.LooseVersion("3.0"):
                if h5py_version == '1.3.1':
                    continue
            versions['pv'] = python_version
            versions['full'] = 'python{pv}-numpy{nv}-h5py{hv}'.format(**versions)
            if version.LooseVersion(numpy_version) >= version.LooseVersion("1.6.2"):
                versions['cc'] = 'clang'
            else:
                versions['cc'] = 'gcc'

            all_versions.append(deepcopy(versions))

from multiprocessing import Pool
p = Pool(processes=24)
p.map(setup_virtualenv, all_versions)
