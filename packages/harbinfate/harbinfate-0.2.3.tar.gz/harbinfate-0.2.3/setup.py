from setuptools import setup, find_packages, find_namespace_packages

setup(
    name='harbinfate',
    version='0.2.3',
    description='A library for doing something cool',
    author='Harbin',
    author_email='harbinfate@gmail.com',
    # url='https://github.com/harbinzhang/',
    # packages=find_namespace_packages(),
    packages=find_packages(),
    # install_requires=
    # packages=['youtube_summary', 'youtube_summary.lib'],
    # packages=['youtube_summary'] + ['youtube_summary.' + p for p in find_packages('lib')],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
