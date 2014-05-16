#!/usr/bin/env python

from distutils.core import setup
from seasondog import info

setup(name='seasondog',
      version=info.VERSION,
      description='Tool for tracking you progress in watching series and playing you the next episode',
      author='Vasiliy Horbachenko',
      author_email='shadow.prince@ya.ru',
      url=info.URL,
      scripts=['seasondog/sdog'],
      packages=['seasondog', ],
     )
