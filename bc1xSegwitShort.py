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
import requests
import bech32

def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


r = 0
cores=2 #<-----------------------------------------------------------change here  CPU


def seek(r, df_handler):
	global num_threads
	LOG_EVERY_N = 10000
	start_time = dt.datetime.today().timestamp()
	i = 0
	print("Core " + str(r) +":  Searching Private Key..")
	while True:
		i=i+1
		# generate private key , Compressed WIF start with K
		priv_key = os.urandom(32)
		fullkey1 = binascii.hexlify(priv_key).decode()
		fullkey = '80' + binascii.hexlify(priv_key).decode() +'01'
		sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
		sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
		WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))

		# get public key , Compressed address starts with "1"
		sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		key_bytes = binascii.hexlify(vk.to_string()).decode()
		key = ('0x' + binascii.hexlify(sk.verifying_key.to_string()).decode('utf-8'))
		half_len = len(key_bytes) // 2
		key_half = key_bytes[:half_len]
		# Add bitcoin byte: 0x02 if the last digit is even, 0x03 if the last digit is odd
		last_byte = int(key[-1], 16)
		bitcoin_byte = '02' if last_byte % 2 == 0 else '03'
		publ_key = bitcoin_byte + key_half
		hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
		#publ_addr_a = bytes.fromhex("0014") + hash160
		#hash160b=ripemd160(hashlib.sha256(publ_addr_a).digest()).digest()
		publ_addr_b =bech32.encode("bc",0,hash160) 
		priv = WIF.decode()
		pub = publ_addr_b
		time_diff = dt.datetime.today().timestamp() - start_time
		if (i % LOG_EVERY_N) == 0:
			print('Core :'+str(r)+" K/s = "+ str(i / time_diff)+ dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

		#print ('Worker '+str(r)+':'+ str(i) + '.-  # '+pub + ' # -------- # '+ priv+' # ')
		pub = pub + '\n'
		filename = '/data/BitBruteForce-Wallet-Compressed-Address/top3M_bc_short.txt' #<----------------------------------------------------------change here Dir
		with open(filename) as f:
			for line in f:
				if pub in line:
					msg = "\nPublic: " + str(pub) + " ---- Private: " + str(priv)
					text = msg
					print(text)
					#requests.post(url="https://maker.ifttt.com/trigger/hmbt/with/key/d8gr-cI50XXn1WSEOHf64W", data={ 'value1' : 'P', 'value2' : fullkey1, 'value3' : 'R3'})
					with open('Wallets.txt','a') as f:
						f.write(priv)
						f.write('     ')
						f.write(pub)
						f.write('\n')
						f.close()
					time.sleep(10)
					print (fullkey1 + 'WINNER WINNER CHICKEN DINNER!!! ---- ' + dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pub, priv)
					break
					



contador=0
if __name__ == '__main__':
	jobs = []
	df_handler = pd.read_csv(open('/data/BitBruteForce-Wallet-Compressed-Address/top3M_bc_short.txt', 'r'))  #<--------------------------------------------------------change here Dir
	for r in range(cores):
		p = multiprocessing.Process(target=seek, args=(r,df_handler))
		jobs.append(p)
		p.start()
