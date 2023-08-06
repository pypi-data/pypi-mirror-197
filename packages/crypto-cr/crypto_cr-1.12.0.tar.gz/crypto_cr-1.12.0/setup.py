from setuptools import setup, find_packages
from os import path

# Abre o arquivo README.md para ler o conteúdo
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='crypto_cr',
    version='1.12.0',
    description="This project refers to a password encryptor, which also serves to encrypt and decrypt files through a password entered by users",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vinicius Nunes & Nara Raquel',
    author_email='viniciusnunes02612@gmail.com ',
    maintainer = "Nara Raquel Dias Andrade",
    maintainer_email = "naradiasspn1967@gmail.com",
    url=' https://github.com/NaraAndrad3/Cripto',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'hashlib ',
        'cryptography',
        'string ',
        'random',
        'hashlib',
    ],
)