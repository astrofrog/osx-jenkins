import os
import urllib
import tarfile

# Set parameters
VERSION = 'mpich2-1.4.1p1'
version_number = '1.4.1p1'
URL = 'http://www.mcs.anl.gov/research/projects/mpich2/downloads/tarballs/1.4.1p1/%s.tar.gz' % VERSION
TARFILE = os.path.basename(URL)
COMPILERS = ['pgfortran', 'gfortran-mp-4.3', 'gfortran-mp-4.4', 'gfortran-mp-4.5', 'gfortran-mp-4.6', 'gfortran-mp-4.7', 'g95', 'ifort']
EXTRA = {}
EXTRA['g95'] = 'CC=gcc-mp-4.4'

# Download file
if not os.path.exists(TARFILE):
    open(TARFILE, 'wb').write(urllib.urlopen(URL).read())

t = tarfile.open(TARFILE, 'r:gz')

start = os.path.abspath('.')

for compiler in COMPILERS:
    if os.path.exists(compiler):
        print "Skipping %s" % compiler
        continue
    else:
        print "Building %s" % compiler
    t.extractall(compiler)
    os.chdir(compiler)
    os.chdir(VERSION)
    extra = EXTRA[compiler] if compiler in EXTRA else ""
    os.system('PATH=/opt/local/bin:/opt/pgi/osx86-64/11.10/bin:$PATH ./configure --enable-fc ' \
              + '--prefix=$HOME/usr/mpich2/%s-%s ' % (compiler, version_number) \
              + 'F77=%s FC=%s %s>& log_configure' % (compiler, compiler, extra))
    os.system('PATH=/opt/local/bin:$PATH make >& log_make')
    os.system('PATH=/opt/local/bin:$PATH make install >& log_make_install')
    os.chdir(start)

