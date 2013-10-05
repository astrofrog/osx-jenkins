import os
import urllib
import tarfile

# Set parameters
VERSION = 'hdf5-1.8.9'
version_number = '1.8.9'
URL = "http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-{version}/src/hdf5-{version}.tar.gz".format(version=version_number)
TARFILE = os.path.basename(URL)
COMPILERS = ['pgfortran', 'gfortran-mp-4.3', 'gfortran-mp-4.4', 'gfortran-mp-4.5', 'gfortran-mp-4.6', 'gfortran-mp-4.7', 'g95', 'ifort']
EXTRA = {}
EXTRA['g95'] = 'CC=gcc-mp-4.4'
PATH = "PATH=/opt/local/bin:/opt/pgi/osx86-64/13.2/bin:$PATH"

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
    if compiler == 'g95':
        s = open('config/gnu-fflags', 'rb').read()
        s = s.replace('-Wconversion', '')
        s = s.replace('-Wunderflow', '')
        open('config/gnu-fflags', 'wb').write(s)
    os.system('{path} ./configure --enable-fortran --enable-hl '
              '--prefix=$HOME/usr/hdf5/{compiler}-{version_number} '
              'FC={compiler} {extra} >& log_configure'.format(path=PATH, compiler=compiler, version_number=version_number, extra=extra))
    os.system('{path} make >& log_make'.format(path=PATH))
    os.system('{path} make install >& log_make_install'.format(path=PATH))
    os.chdir(start)

