from setuptools import setup, find_packages

setup(
    name='JohnServerAPI',
    version='0.0.1',
    description='This is a module to interact with Server and Client',
    author='John',
    author_email='myemail@example.com',
    install_requires=[
        'requests',
        'numpy',
        'matplotlib',
        'socket',
        'socketserver',
        'ipaddress',
        'tkinter'
    ],
    long_description=open("ReadMe.md").read(), 
     long_description_content_type="text/markdown",
)
