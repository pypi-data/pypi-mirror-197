from cryptography.fernet import Fernet #biblioteca que fornece suporte a algoritmos de criptografia
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
import os
import hashlib
import string
import random

class Generate:
    def __init__(self) -> None:
        pass

    def password_letters(self,tam): 
        char = string.ascii_letters #cria uma string com todas as letras do alfabeto
        password = '' # string onde será criada a senha
        # vai escolher aleatoriamente um caractere da string char a partir do random.choice e ir 
        # concatenando até formar a senha do tamanho desejado
        for i in range(tam):
            password += random.choice(char) # a função choice retorna um elemnto aleatoria da string
        return password

    def pwd_LettersNumbers(self,tam): 
        char = string.ascii_letters + string.digits #cria uma string com todas as letras do alfabetot = Teste()
        password = '' # string onde será criada a senha
        # vai escolher aleatoriamente um caractere da string char a partir do random.choice e ir 
        # concatenando até formar a senha do tamanho desejado
        for i in range(tam):
            password += random.choice(char) # a função choice retorna um elemnto aleatoria da string
        return password
    
    def password_numbers(self,tam): 
        char = string.digits #cria uma string com "todos" os numeros
        password = '' # string onde será criada a senha
        # vai escolher aleatoriamente um caractere da string char e ir 
        # concatenando até formar a senha do tamanho desejado
        for i in range(tam):
            password += random.choice(char) # a função choice retorna um elemnto aleatoria da string
        return password #vai retornar uma senha numeria de tipo int 
    

    def punctuation(self,tam):
        char = string.ascii_letters + string.digits + string.punctuation
        password = ''
        
        for i in range(tam):
            password = ''.join(random.choice(char))
        return password

    def noRepetition(self,tam):
        passNumeric = range(tam)
        strPassword = ''.join(map(str,passNumeric))
        return strPassword


    def pronounciablePassword(self,tam):
        vogais = 'aeiou'
        consoantes = "bcdfghjklmnpqrstvwxyz"
        password = ''
        for i in range(tam):
            if i %2 == 0:
                password += ''.join(random.choice(vogais))
            else:
                password += ''.join(random.choice(consoantes))
        return password

    def password_hash(self,pwd):
        password = hashlib.md5()
        password.update(pwd)
        return password.hexdigest()
        

class FilesDec:
    def __init__(self):
        pass

    def encryptPassword(self, pwd):
        password = pwd.encode()
        salt = bytes('ç/@&%)+LK~qer!?#(<>:;/\|-','utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def extensionChange(self, filename):
        file = ""
        for i in filename:
            if i == ".":
                break
            else:
                file += i

        return file

    def encryptFile(self, filename, pwd):
        encryptKey = self.encryptPassword(pwd)

        fileKey = self.extensionChange(filename) + ".key"

        with open(fileKey, "wb") as fileK:
            fileK.write(encryptKey)

        with open(filename, "rb") as f:
            file = f.read()

        enc = Fernet(encryptKey)

        encriptedData = enc.encrypt(file)

        with open(filename, "wb") as encryptyFile:
            encryptyFile.write(encriptedData)
        
        return fileKey

    def decryptFiles(self, filename, pwd):
        fileKey = self.extensionChange(filename) + ".key"

        with open(fileKey, "rb") as fk:
            key = fk.read()

        encriptedKey = self.encryptPassword(pwd)
        print('chave: ',encriptedKey)
        if encriptedKey != key:
            print('Erro ao descriptar arquivo. senha incorreta')
        else:
            enc = Fernet(key)

            with open(filename, "rb") as f:
                file = f.read()

                decryptedData = enc.decrypt(file)

            with open(filename, "wb") as fileDecrypted:
                fileDecrypted.write(decryptedData)




    
    