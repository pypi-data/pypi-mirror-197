from setuptools import setup, find_packages

setup(
    name='hppmodule',
    version='0.1.5',
    author='Papa',
    author_email='htunpa2aung@gmail.com',
    description='Testing packages by Papa',
    packages=['hppmodule'],
    install_requires=[
        'requests',
        'flask',
    ],
)

