from setuptools import setup

classifiers=[
        'Development Status :: Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Metadata',
    ]
install_requires = [
]
setup(
    name='autometa',
    version='0.0.1',
    author='Ashutosh Bhudia',
    author_email='ashu.bhudia@gmail.com',
    license='Apache License, Version 2.0',
    classifiers=classifiers,
    platfroms=['MacOS X', 'Linux', 'Windows'],
    install_requires=install_requires,
    packages=['autometa']
)