from setuptools import setup, find_packages

setup(
    name='pp_api',
    version='0.1.2',
    author='Papa',
    author_email='htunpa2aung@gmail.com',
    description='Testing packages by Papa',
    packages=['pp_api'],
    install_requires=[
        'requests',
        'flask',
    ],
)

