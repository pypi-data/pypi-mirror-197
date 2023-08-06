from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='flask-cache-manifest',
    packages=['flask_cache_manifest'],
    version='1.0.0',
    author='Maxime Dupuis',
    author_email='mdupuis@hotmail.ca',
    url='https://github.com/maxdup/flask-cache-manifest',
    description='Flask extension to serve md5 hashed assets.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    platforms='any',
    python_requires='>=3.6',
    install_requires=[
        'Flask>=2.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Compression'
    ]
)
