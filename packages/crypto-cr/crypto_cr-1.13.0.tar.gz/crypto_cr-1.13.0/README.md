# CRYPTO_CR
==========



This project refers to a password encryptor, which also serves to encrypt and decrypt files through a password entered by users. <br>
[Project Cripto](https://github.com/NaraAndrad3/Cripto/)
to write your content.


<h3><li>1 - Para instalar o pacote use:</li></h3>

``````
pip install crypto_cr
``````


<h3><li>2 - import o modulo usando:</li></h3>

``````
from crypto_cr import *
``````



<h3><li>3 - Formas de usar o pacote:</li></h3>

``````
#Encriptando e decriptando o arquivo

f = FilesDec()



print('Criptografar: ')
arq = 'arquivo.pdf'
f.encryptFile(arq,'1234')


print('Decriptografar: ')
f.decryptFiles(arq,'1234')


#Gerando senhas
senha1 = pwd.password_letters(8)

``````
