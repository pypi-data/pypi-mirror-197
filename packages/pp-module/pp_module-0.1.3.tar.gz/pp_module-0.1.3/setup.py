from setuptools import setup, find_packages

setup(
    name='pp_module',
    version='0.1.3',
    author='Papa',
    author_email='htunpa2aung@gmail.com',
    description='Testing packages by Papa',
    packages=['pp_module'],
    install_requires=[
        'requests',
        'flask',
    ],
)

