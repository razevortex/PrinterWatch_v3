
from setuptools import setup

setup(
        name="printerwatch",
        version="1.0",
        description="package used to track printer data and use them in a django application",
        author="razevortex",
        author_email="razevortex@googlemail.com",
        packages=["/srv/servme/printerwatch"],
        install_requires=['django','bs4', 'pyotp', 'qrcode']
        )
