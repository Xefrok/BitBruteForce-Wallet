# BitBruteForce-Wallet
This is a little but effective script to Brute Force the Private Key of any Bitcoin Public Address.

How this script works?
Very easy.

Every code i saw for the last year just generate randomly private and public address and check the balance (very, very slow for the API Request)

So, i found **123,000 Bitcoin Addresses** with 1+ BTC from 2009 to 2013 and NEVER made a transaction, so, lost BTC...
like huge pirates boats at the ocean bottom full of treasures.

This Script create randomly private and public address without checking the balance, instead of making API Request, the created public addresses compare it with the list i have.

So, short long story.
Create Random Public Address (**RPA**) and check one by one with the Public Address (**PA**) at the list

**if RPC == PA then
	YOU WINNED THE LOTTREY!
else
	KEEP SEARCHING MTF!**
	
(Script tested on i7-4500U 8 Cores - 5 K/s per Core. 3,456,000 Private Keys generated per day)

i think is quite simple.

If you like it!! **1KyQXpa1Zke5v94QZV2U77i7oaVwPTijdY**


REQUERIMENTS
=

 - Python 3.x (i use 3.6.5)
 - pip install ecdsa
 - pip install base58
 - 3,000,000,000 Years

