import os
import shutil

for version in ['2.6.8', '2.7.3', '3.1.5', '3.2.3', '3.3.0'][-1:]:

    short_version = version[:3]

    if os.path.exists('Python-{0:s}'.format(version)):
        shutil.rmtree('Python-{0:s}'.format(version))

    os.system('tar xvzf Python-{0:s}.tgz'.format(version))

    os.chdir('Python-{0:s}'.format(version))
    if version == '3.3.0b2':
        os.system('CC=clang ./configure --prefix=$HOME/usr/python ; make ; make install')
    else:
        os.system('./configure --prefix=$HOME/usr/python ; make ; make install')
    os.chdir('..')

    shutil.rmtree('Python-{0:s}'.format(version))

    if os.path.exists('distribute-0.6.27'):
        shutil.rmtree('distribute-0.6.27')

    os.system('tar xvzf distribute-0.6.27.tar.gz')
    os.chdir('distribute-0.6.27')
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('distribute-0.6.27')

    if os.path.exists('pip-1.1'):
        shutil.rmtree('pip-1.1')

    os.system('tar xvzf pip-1.1.tar.gz')
    os.chdir('pip-1.1')
    os.system('$HOME/usr/python/bin/python{0:s} setup.py install'.format(short_version))
    os.chdir('..')

    shutil.rmtree('pip-1.1')

    os.system('$HOME/usr/python/bin/pip-{0:s} install virtualenv'.format(short_version))

