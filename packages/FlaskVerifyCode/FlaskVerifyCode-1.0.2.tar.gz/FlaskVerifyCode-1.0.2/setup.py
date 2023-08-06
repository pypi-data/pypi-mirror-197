import setuptools
from distutils.core import  setup

packages = ['FlaskVerifyCode']

ALL = [
    'flask',
    'itsdangerous',
    'Werkzeug',
    'Jinja2'
]

setup(
    name='FlaskVerifyCode',
    version='1.0.2',
    author='FlaskVerifyCode',
    description='Flask mini verification code receiving verification interface',
    author_email='me@lyshark.com',
    python_requires=">=3.6.0",
    license = "MIT Licence",
    packages=packages,
    include_package_data = True,
    platforms = "any",
    extras_require={
    "all": ALL
    }
    )
