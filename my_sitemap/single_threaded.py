from bs4 import BeautifulSoup

import re

import requests
#url = 'https://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-using-python'
#sitename = 'https://stackoverflow.com'

url = 'https://crawler-test.com'
sitename = 'https://crawler-test.com'

FOUNDS = dict()
TOPROCESS = list()
PROCESSED = 0
TOTAL = 0
DUPLICATES = 0

def ScanAlso(url, sitename) :
    global DUPLICATES, TOTAL, FOUNDS
    dupl = 0
    uniq = 0
    
    #print('Загружаю...')
    page = requests.get(url).text 
    #print('Загружено.Обрабатываю хтмл')
     
    soup = BeautifulSoup(page)
    #print('Обработано.Ищу все ссылки <a href...>tag')

    foundsAlinks = soup.findAll('a')
    #print('фильтрую...')

    
    for link in foundsAlinks :
        addr = link.get('href')
        if  addr is None: continue
        if ( not isinstance(addr, str)): continue
        if  len(addr)<=2: continue

        #work with short links   eg /teams  /about_us 
        if addr[0]=='/': addr = sitename + addr #eg http:/stackoverflow.com/teams
        if addr[-1]=='/': addr = addr[0:-1]

        
        if '#' in addr:            
            hashPoz = addr.index('#')
            addr = addr[0:hashPoz]

        
        if 'http' not in addr:
            continue


        if addr not in FOUNDS.keys():
            FOUNDS[addr] = -1
            TOPROCESS.append(addr)
            uniq+=1
        else:
            DUPLICATES+=1
            dupl+=1
    print('\t\t\tAdded '+str(uniq)+' elm, dupl:'+str(dupl) )
    TOTAL += uniq

ScanAlso(url, sitename)





##########
#
#       DO WORK =)
#
########


IN_STOCK= -1
IN_PROCESSING = 0
IN_DONELIST = 1


while (len(TOPROCESS)>0) :
    link=TOPROCESS.pop(0)
    key = link
    status = FOUNDS[key]
     
    
    #print(str(status) + ' = '+ link)
    if status == IN_STOCK:
        FOUNDS[key]= IN_PROCESSING
        ScanAlso(link, sitename)
        FOUNDS[key]= IN_DONELIST
        PROCESSED +=1
    print(str(PROCESSED)+'/'+str(TOTAL) + ' (DD='+str(DUPLICATES)+')')
    #input('...')
    
        













