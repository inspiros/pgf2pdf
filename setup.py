from setuptools import find_packages
from setuptools import setup


setup(
    name="pgf2pdf",
    version="1.0",
    author="inspiros",
    author_email='hnhat.tran@gmail.com',
    description="pgf to pdf converter",
    packages=find_packages(exclude=("example",)),
    entry_points={
        'console_scripts': [
            'pgf2pdf = pgf2pdf.main:main',
        ],
    },
)
