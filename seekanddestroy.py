#!/usr/bin/python

'''
Change Cores=# of how many cores do you want to use (Script tested on i7-4500U 8 Cores - 5 K/s per Core. 3,456,000 Private Keys generated per day)

Take into account VM as well (i3 with 2 cores but 4VM -> 8 threads). More cores is just more demanding for OS scheduler
(worth playing around, even above number of CPU cores)
'''

import time
import datetime as dt
import smtplib
import os
import multiprocessing
from multiprocessing import Pool
import binascii, hashlib, base58, ecdsa
import pandas as pd


def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


r = 0
cores=6


def seek(r, df_handler):
	global num_threads
	LOG_EVERY_N = 1000
	start_time = dt.datetime.today().timestamp()
	i = 0
	print("Core " + str(r) +":  Searching Private Key..")
	while True:
		i=i+1
		# generate private key , uncompressed WIF starts with "5"
		priv_key = os.urandom(32)
		fullkey = '80' + binascii.hexlify(priv_key).decode()
		sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
		sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
		WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))

		# get public key , uncompressed address starts with "1"
		sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
		hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
		publ_addr_a = b"\x00" + hash160
		checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
		publ_addr_b = base58.b58encode(publ_addr_a + checksum)
		priv = WIF.decode()
		pub = publ_addr_b.decode()
		time_diff = dt.datetime.today().timestamp() - start_time
		if (i % LOG_EVERY_N) == 0:
			print('Core :'+str(r)+" K/s = "+ str(i / time_diff))
		#print ('Worker '+str(r)+':'+ str(i) + '.-  # '+pub + ' # -------- # '+ priv+' # ')
		pub = pub + '\n'
		filename = 'bit.txt'
		with open(filename) as f:
			for line in f:
				if pub in line:
					msg = "\nPublic: " + str(pub) + " ---- Private: " + str(priv) + "YEI"
					text = msg
					#UNCOMMENT IF 2FA from gmail is activated, or risk missing your winning ticket;)
					#server = smtplib.SMTP("smtp.gmail.com", 587)
					#server.ehlo()
					#server.starttls()
					#server.login("example@gmail.com", "password")
					#fromaddr = "example@gmail.com"
					#toaddr = "example@gmail.com"
					#server.sendmail(fromaddr, toaddr, text)
					print(text)
					with open('Wallets.txt','a') as f:
						f.write(priv)
						f.write('     ')
						f.write(pub)
						f.write('\n')
						f.close()
					time.sleep(30)
					print ('WINNER WINNER CHICKEN DINNER!!! ---- ' +dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pub, priv)
					break
					



contador=0
if __name__ == '__main__':
	jobs = []
	df_handler = pd.read_csv(open('bit.txt', 'r'))
	for r in range(cores):
		p = multiprocessing.Process(target=seek, args=(r,df_handler))
		jobs.append(p)
		p.start()

