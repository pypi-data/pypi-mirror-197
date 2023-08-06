from distutils.core import setup

setup(
    name='PyWinRD',
    packages=['PyWinRD'],
    version='1.4.6.2',
    license='MIT',
    description='Python library that provides remote debugging capabilities for python files between two windows machines, the library supports logging of '
                'clients activities and redirecting all the print and input operations to the client and shadowing them in the server.',
    author='AhmedAhmedEG',
    author_email='ahmedahmed.abdelmaksoud.eg@gmail.com',
    url='https://github.com/AhmedAhmedEG/PyWinRD',
    download_url='https://github.com/AhmedAhmedEG/PyWinRD/archive/refs/tags/1.4.6.2.tar.gz',
    keywords=['Remote Debugging', 'Python', 'Windows'],
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
