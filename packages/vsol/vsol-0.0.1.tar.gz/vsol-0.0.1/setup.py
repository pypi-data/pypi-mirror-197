from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Typing :: Typed',
    'Topic :: Utilities',
]

setup(
    name='vsol',
    version='0.0.1',
    description='VSOL is a simple, human-readable, and easy-to-use configuration file format.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Md. Almas Ali',
    author_email='almaspr3@gmail.com',
    url='https://github.com/vsol-lang/vsol',
    license='MIT',
    packages=find_packages(),
    classifiers=classifiers,
    python_requires='>=3.8',
    install_requires=[],
)
