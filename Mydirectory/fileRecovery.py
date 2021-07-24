import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad

file_out = open("ransomkey.bin")
private_key = RSA.import_key(file_out.read())
Encfiles = []

#function  to find enc files in the directory
def findEnc():
	#first check if the file is a "file" and ensure that it is a .enc file
	for file in os.listdir("."):
		if os.path.isfile(file):
			if file.endswith(".enc"):
				#save these .enc files in a list to use later
				Encfiles.append(file)
	Encfiles.sort()
findEnc()
#function to decrypt the data in .enc files
def decryptData():
	#open the file to read encrypted session key and associated iv for each encrypted file
	file_read = open("encrypted_session_keys.bin","rb")
	for file in Encfiles:
		with open(file, "rb") as file_out:
			#read the encrypted session key from the file "encrypted_session_keys.bin"
			encrypted_session_key = file_read.read(private_key.size_in_bytes())
			#use the RSA private key to decrypt encrypted session key
			cipher=PKCS1_OAEP.new(private_key)
			session_key=cipher.decrypt(encrypted_session_key)
			#read the iv associated with each encrypted file from the file 			"encrypted_session_keys.bin"
			iv=file_read.read(16)
			#read the encrypted data from .enc encrypted file
			encryptedData=file_out.read()
			#use iv, session key to decrypt the file and its data, unpad data to get text 				content
			cipherD=AES.new(session_key,AES.MODE_CBC,iv=iv)
			pt=unpad(cipherD.decrypt(encryptedData), AES.block_size)
			data=pt.decode("utf-8")
		#create the .txt files with decrypted data
		with open(file[:-4] + ".txt", "w") as file_out:
			file_out.write(data)
			file_out.close()
decryptData()		
#function will delete the encrypted files, encrypted session keys and iv file, RSA private key and public key file from the folder
def deleteForever():
	os.unlink("encrypted_session_keys.bin")
	os.unlink("ransomkey.bin")
	os.unlink("public.pem")
	for filename in os.listdir():
		if filename.endswith(".enc"):
			os.unlink(filename)
deleteForever()
			
