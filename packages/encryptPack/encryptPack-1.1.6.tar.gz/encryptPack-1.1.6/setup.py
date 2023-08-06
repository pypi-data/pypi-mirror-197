from setuptools import setup


with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='encryptPack',
    version='1.1.6',
    url='https://github.com/NaraAndrad3/crypto',
    license='MIT License',
    author='Nara Raquel e Vinicius Nunes',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='naradiasspn1967@gmail.com',
    maintainer= 'Vinicius Nunes',
    maintainer_email= 'viniciusnunes02612@gmail.com',
    keywords='Password',
    description=u'Pacote para geração e criptografia de senhas, criptografia e descriptografia de arquivos',
    packages= ['CryptoPwd'],
    install_requires=['cryptography'],
 )

