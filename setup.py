#!/usr/bin/env python

from distutils.core import setup

VERSION = (0, 2, 0)

setup (
    name="mfp",
    version="%d.%d.%d" % VERSION,
    description="multi format packager",
    author="James Tanner",
    author_email="tanner.jc@gmail.com",
    license="Apache License 2.0",
    packages=[
        'mfp',
        'mfp.lib',
    ],
    scripts=['mfp/bin/mfp'],
    )

