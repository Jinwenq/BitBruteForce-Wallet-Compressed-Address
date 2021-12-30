# BitBruteForce-Wallet (Only uncompressed Addess!)
This is an effective script to Brute Force, the Private Key of any Bitcoin Public Address.

How does the script work? 
Very easy.

Every code I´ve seen for the last year just generates randomly private and public addresses and checks the balance (very, very slow for the API Request).



This Script creates randomly private and public addresses without checking the balance, instead of making API Request, the created Public Address is compared with the list I own.

Long story short. 
Create Random Public Address (**RPA**) and check one by one with the Public Address (**PA**) at the list.

**if RPC == PA then
	YOU WINNED THE LOTTREY!
else
	KEEP SEARCHING MTF!**
	
(Script tested on i7-4500U 8 Cores - 16.32 K/s per Core. 11,280,384 Private Keys generated per day)

REQUERIMENTS
=

 - Python 3.x (i use 3.6.5)
 - !wget http://addresses.loyce.club/Bitcoin_addresses_LATEST.txt.gz
 - !gzip -d /content/Bitcoin_addresses_LATEST.txt.gz
 - !git clone https://github.com/Jinwenq/BitBruteForce-Wallet.git - 
 - !pip install ecdsa
 - !pip install base58
 - !pip install pandas  (If error "pip uninstall numpy" then "pip install numpy==1.19.3")
 - !python3 /content/BitBruteForce-Wallet/seekanddestroy.py

