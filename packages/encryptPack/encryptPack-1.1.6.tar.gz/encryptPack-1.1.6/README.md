# encryptPack
=============

This project refers to a password encryptor, which also serves to encrypt and decrypt files through a password entered by users. <br>


[Project Cripto](https://github.com/NaraAndrad3/CryptoPack)to write your content.

<h3><li>1 - Para instalar o pacote use:</li></h3>

``````
pip install encryptPack
``````
<h3><li> 2 - import o modulo usando: </li></h3>

``````https://github.com/NaraAndrad3/Cripto/tree/main/Package
from CryptoPwd import crypt

``````

<h3><li>3 - Formas de usar o pacote:</li></h3>

``````
from CryptoPwd import crypt

#instancia da classe FileDesc
f = crypt.FilesDec() 

# Criptografando um arquivo
f.decryptFiles('teste.txt','1234')

#Decriptografando um arquivo
f.decryptFiles('teste.txt','1234')

``````