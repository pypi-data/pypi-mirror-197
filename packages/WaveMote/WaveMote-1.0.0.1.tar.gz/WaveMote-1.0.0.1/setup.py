from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name = 'WaveMote',
    version= '1.0.0.1',
    description= 'A Gestures based Hand Controlled Virtual Mouse',
    long_description= long_description,
    long_description_content_type='text/markdown',
    url= 'https://github.com/bharathguntreddi3/Hand-Controlled-AI-Virtual-Mouse',
    author= 'Bharath Guntreddi',
    author_email= 'guntreddibharath@gmail.com',
    license= 'MIT',
    classifiers= classifiers,
    keywords= 'WaveMote',
    packages= ['WaveMote'],
    install_requires= ['']
)