import os

COMPILERS = [('/opt/pgi/osx86-64/13.2/bin/pgfortran','/usr/bin/gcc'),
             ('/opt/local/bin/gfortran-mp-4.3','/opt/local/bin/gfortran-mp-4.3'),
             ('/opt/local/bin/gfortran-mp-4.4','/opt/local/bin/gfortran-mp-4.4'),
             ('/opt/local/bin/gfortran-mp-4.5','/opt/local/bin/gfortran-mp-4.5'), 
             ('/opt/local/bin/gfortran-mp-4.6','/opt/local/bin/gfortran-mp-4.6'),
             ('/opt/local/bin/gfortran-mp-4.7','/opt/local/bin/gfortran-mp-4.7'),
             ('/opt/local/bin/g95', '/opt/local/bin/gcc-mp-4.4'),
             ('/usr/bin/ifort', '/usr/bin/gcc')]

def install(compiler):
    os.system('python install_deps.py --fc-compiler={fc} --cc-compiler={cc} $HOME/usr/fortran_deps/{prefix} >& {prefix}.log'.format(fc=compiler[0], cc=compiler[1], prefix=os.path.basename(compiler[0])))

import multiprocessing as mp
p = mp.Pool(processes=8)
p.map(install, COMPILERS)
