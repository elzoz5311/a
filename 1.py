#!/usr/bin/env
# -*- coding: utf-8 -*-
import sys , requests , re
from multiprocessing.dummy import Pool
from colorama import Fore								
from colorama import Style								
from pprint import pprint								
from colorama import init										
init(autoreset=True)

fr  =   Fore.RED																					
fg  =   Fore.GREEN	

print """  
 _  _  _                _                            
| || || |              | |                           
| || || | ___   ____ _ | |____   ____ ____  ___  ___ 
| ||_|| |/ _ \ / ___) || |  _ \ / ___) _  )/___)/___)
| |___| | |_| | |  ( (_| | | | | |  ( (/ /|___ |___ |
 \______|\___/|_|   \____| ||_/|_|   \____|___/(___/ 
                         |_|                         
"""

try:
    target = [i.strip() for i in open(sys.argv[1], mode='r').readlines()]
except IndexError:
	path =  str(sys.argv[0]).split('\\')
	exit('\n  [!] Enter <'+path[len(path)-1] + '> <sites.txt>')
	

def URL(url):
	if url[-1] == "/":
		pattern = re.compile('(.*)/')
		site = re.findall(pattern,url)
		url = site[0]
	if url[:7] != "http://" and url[:8] != "https://":
		url = "http://" + url
	return url	
	
	
def filter(site):
	pet = re.compile('<meta name="generator" content="(.*)" />')
	try:
		site = URL(site)
		src = requests.get(site,timeout=15).content
		if re.findall(pet,src):
			generator = re.findall(pet,src)[0]
			if 'WordPress' in generator :
				print ' --| '+site +' --> {}[WordPress]'.format(fg)
				with open('wordpress.txt', mode='a') as d:
					d.write(site+'/\n')
			else :
				if 'wp-content/themes' in src :
					print ' --| '+site +' --> {}[WordPress]'.format(fg)
					with open('wordpress.txt', mode='a') as d:
						d.write(site+'/\n')
				else :
					print ' --| '+site +' --> {}[Other]'.format(fr)
					with open('other.txt', mode='a') as d:
						d.write(site+'/\n')
		else :
			if 'wp-content/themes' in src :
				print ' --| '+site +' --> {}[WordPress]'.format(fg)
				with open('wordpress.txt', mode='a') as d:
					d.write(site+'/\n')
					
			else :
				print ' --| '+site +' --> {}[Other]'.format(fr)
				with open('other.txt', mode='a') as d:
					d.write(site+'/\n')			
	except :
		print ' --| '+site +' --> {}[Time Out]'.format(fr)
		
mp = Pool(150)
mp.map(filter, target)
mp.close()
mp.join()		
