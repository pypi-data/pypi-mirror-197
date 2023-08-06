import sys
from setuptools import setup

if sys.version_info[:2] < (3, 8):
    error = ('post_processing_pupil requires Python 3.8 or later (%d.%d detected).' % sys.version_info[:2])
    sys.stderr.write(error + "\n")
    sys.exit(1)

# General informations
name = 'post_processing_pupil'
version = '0.1.3'
description = 'Python package to calculte output fixation points produced by the pupil-core eye tracker'
url = 'https://github.com/LostInZoom/post_processing_ET'
author = 'Laura Wenclik'
author_email = 'laura.wenclik@ign.fr'
lic = 'GPLv3'
packages = [
    'post_processing_pupil'
]

# Requirements and dependencies
python_requires = '>=3.8'
install_requires = [
    'pandas',
]

# Meta informations
keywords = [
    'pupil core',
    'eye tracker',
]
platforms = ['Linux', 'Mac OSX', 'Windows', 'Unix']
classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only',
]

if __name__ == '__main__':
    setup(
        name=name,
        version=version,    
        description=description,
        url=url,
        author=author,
        author_email=author_email,
        license=lic,
        packages=packages,
        python_requires=python_requires,
        install_requires=install_requires,
        keywords = keywords,
        platforms = platforms,
        classifiers=classifiers,
    )