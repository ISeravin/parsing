 
#Parser
from bs4 import BeautifulSoup
import re
import requests


#Threading
import queue
import threading
import time
from random import randrange
 
THREADS =  queue.SimpleQueue()
LINKS = queue.SimpleQueue()


buebue = False
deads = 0
threads = 5
puts = 0
conflicts = 0

progUID = str(randrange(91,99))
CONSOLES = [  queue.SimpleQueue() , queue.SimpleQueue() ]
consoleSwap = False




#Parsing-----------
url = 'https://crawler-test.com/'
sitename = 'https://crawler-test.com'

url = 'https://stackoverflow.com/questions/3075550/how-can-i-get-href-links-from-html-using-python'
sitename = 'https://stackoverflow.com'
   
        
buebue = False
import queue

FOUNDS = dict()
FOUNDS_RQ = queue.SimpleQueue()
FOUNDSLOCK = threading.Lock()
TOPROCESSLOCK = threading.Lock()



TOPROCESS = list() 


PROCESSED = 0
ERRSKIPPED = 0
TOTAL = 0
DUPLICATES = 0

    
def checkIfDie():
    return buebue==True

def get_QueuePro(QQ,block=True, delay = 0.1) :
  while True:
      try:
          if not must and checkIfDie():
              return 0
          QQ.get(elm,True,delay)
          return 0 
      except :
        return 100

      return 1  

                  
def putToQueuePro(QQ, elm, block=True, delay = 0.1, must=False):
   
  while True:
    try:
        if not must and checkIfDie():
            return 0
        QQ.put(elm,True,delay)
        return 0 
    except :
      time.wait(0.0001)

    return 1


def putToQueueSoftly(QQ, elm):   
    try:
        QQ.put_nowait(elm)
        return 0 
    except:
       return -1

 

def printPro(text,must=False):
  global activeConsole
  while True:
    try:
      if not must and buebue==True:
        break;
      CONSOLES[consoleSwap].put(text,True,0.5)
      break
    except:
      time.wait(0.1)

    


def link_hash(link):
    numbe = 0
    for letter in link:
        numbe += ord(letter)
    numbe = '<H'+ str(round(numbe // 2056))+'.'+str(round(numbe % 2056 ))+ '>'
    return numbe     


# do_work
def ScanAlso(urlIN, sitename, threadUID, lim=None,dieAfterEmptySec = 5) :
    curlim = lim
    cur_dieAfterEmptySec = dieAfterEmptySec
    url=urlIN
    global LINKS, deads, puts, conflicts
    numof_URL_proccessedbyThisThread = 1
    global DUPLICATES, TOTAL, FOUNDS
    while not checkIfDie():
      
      #printPro( str(threadUID)+' \t\t\t'+link_hash(url)+' \t'+url, must = True  )
      dupl = 0
      uniq = 0
      #print('Загружаю...')

      if checkIfDie(): return 0
      page = requests.get(url).text 
      #print('Загружено.Обрабатываю хтмл')

      if checkIfDie(): return 0
      soup = BeautifulSoup(page)
      #print('Обработано.Ищу все ссылки <a href...>tag')

      if checkIfDie(): return 0
      foundsAlinks = soup.findAll('a')
      #print('фильтрую...')

      found_Atags_onPage = len(foundsAlinks)
      processed_Atags_onPage = 0
      for link in foundsAlinks :
          processed_Atags_onPage+=1
          if checkIfDie(): return 0
          
          addr = link.get('href')
          if  addr is None: continue
          if ( not isinstance(addr, str)): continue
          if  len(addr)<=2: continue

          #work with short links   eg /teams  /about_us 
          if addr[0]=='/home': addr = sitename + addr #eg http:/stackoverflow.com/teams
          if addr[-1]=='/': addr = addr[0:-1]

          
          if '#' in addr:            
              hashPoz = addr.index('#')
              addr = addr[0:hashPoz]

          
          if 'http' not in addr:
              continue

          if checkIfDie(): return 0

                  
          
          
           
          
          PageDone = False
          if  (processed_Atags_onPage== found_Atags_onPage):
            PageDone = True
            
            
          FOUNDSLOCK.acquire()
          try:


             

                  
              if addr not in FOUNDS.keys():
                    FOUNDS[addr] = -1
                    TOPROCESS.append(addr)
                    #putToQueuePro(TOPROCESSQQ, addr)#TOPROCESS.append(addr)
                    uniq+=1
                    puts+=1
              else:
                    DUPLICATES+=1
                    dupl+=1

                  
          finally:
            
               LimAllows = False

               if lim is None:
                 LimAllows = True
               else:
                 if  isinstance(lim, str) and  lim==ONLY_ONE :
                   LimAllows = False
                 elif isinstance(lim, int):
                   if curlim>=0:
                     LimAllows = True
                   
                   
                 
               
               canloadnext = True
               canloadnext = canloadnext and PageDone
               canloadnext = canloadnext and LimAllows

               # только когда вся старнцим обработана  
               # и лимит позволяет
               # - попробуем загрузить следующую ссылку.  если она есть
                              #PageDone and and lim != ONLY_ONE and curlim>=0
              
                 
               if canloadnext:
       
                  
                  if  curlim==0:
                    printPro( str(threadUID)+'. LIMIT GONE..', must = True  )
                    FOUNDSLOCK.release()
                  
                    break


                  
                 #print('curlim=',curlim)
                  while len(TOPROCESS)<=0 :
                    FOUNDSLOCK.release()
                    cur_dieAfterEmptySec-=1
                    if cur_dieAfterEmptySec<=0:
                        break
                    #time.wait(2) 
                    FOUNDSLOCK.acquire()

                    
                  url = TOPROCESS.pop(0)
                  if isinstance(lim, int):
                    curlim-=1
                  numof_URL_proccessedbyThisThread +=1
                  
               FOUNDSLOCK.release()
               if checkIfDie(): return 0
          
          #printPro(str(threadUID)+'=>' + addr  )
          if checkIfDie(): return 0 
         

      time.sleep(2)        
      if checkIfDie(): return 0                 
      #printPro('\t\t\t' + str(threadUID)  + ': Added '+str(uniq)+' elm, dupl:'+str(dupl) )
      TOTAL += uniq
      
      if lim == ONLY_ONE:
        break
      if cur_dieAfterEmptySec<=0:
        break
    printPro( str(threadUID)+'. Dead:', must = True  )
    time.sleep(2)
    if checkIfDie(): return 0        



def readKB():
    global buebue, consoleSwap
    while True:
      if deads == threads:
          break 

       

      
      for i in range(10):
        
        time.sleep(1)
        if i==0:
            #  отчет
            
            print('Мертвы:', deads, ', получено:', puts, ' задержки:',conflicts , '',)
            
        else:
            #
          
            #  наша альтерконсоль
            oldSwitch = consoleSwap
            consoleSwap = not consoleSwap
                
            
            
            trytoreadNoMoreThen = 50
            while True:
              try:
                if CONSOLES[oldSwitch].empty():
                  break
                
                getline= CONSOLES[oldSwitch].get(True, 0.01)
                
                print(getline)
                trytoreadNoMoreThen-=1
                if trytoreadNoMoreThen<=0:
                  oldBox = CONSOLES[oldSwitch] 
                  CONSOLES[oldSwitch] = ''
                  CONSOLES[oldSwitch] = queue.SimpleQueue()
                  del oldBox
                  
                  break
                


              except queue.Empty:
                #ok. done
                 
                break

              
              except BaseException as err:
                print(f"raised {err=}, {type(err)=}")
                time.sleep(1)
                print(':(')


                
 
        if i==9:
          print('ВСЕГО В ПРОЦЕССИНГЕ ', len(TOPROCESS), ', уникальных :', TOTAL, ',пропущено  дублей:',DUPLICATES  , '',)
            
          
          #   ручное принудительно завершение
          useranswer = input('type x to break')
          print('ВСЕГО В ПРОЦЕССИНГЕ ', len(TOPROCESS), ', уникальных :', TOTAL, ',пропущено  дублей:',DUPLICATES  , '',)
          print('received=<'+useranswer+'>',sep='')
          if useranswer=='s':
              FOUNDSLOCK.acquire()
              try:
                 with open('C:\Data\iVanThreadingPy\log.txt', mode='w', encoding='utf-8') as f:
                     txtt =   '\n'.join(  FOUNDS.keys()  )
                     f.write( txtt  ) #(links to file)
                     
                 
              finally:
                  FOUNDSLOCK.release()

                  
              if useranswer=='x':
                buebue = True
                print('buebue=',buebue)
   



  



##########
#
#       DO WORK =)
#
########

ONLY_ONE = 'ONLY_ONE'

IN_STOCK= -1
IN_PROCESSING = 0
IN_DONELIST = 1


LIVESTREAMS = 0
DEADS = 0
LISTENER =threading.Thread(target=readKB, args=()  ) 
LISTENER.start()
'''
FEEDER = threading.Thread(target=readKB, args=()  )
FEEDER.start()
'''


'''#TODO LOCK TOPROCESSLOCK? out of here:
  FOUNDSLOCK.acquire()
  try:
      LIVESTREAMS-=1
      DEADS+=1 
       
  finally:
      nextTOPROCESSlink=
      FOUNDSLOCK.release()
  printPro(str(num)+'=>' + addr  )

'''  


def Do():
  global url, TOPROCESS,FOUNDS,PROCESSED,TOTAL,ERRSKIPPED
 
 
  ScanAlso(url, sitename, 'FOREHEAD', ONLY_ONE)

  curthreads = 0
  print('Starting THREADS...')
  potokN = 0
  while curthreads<threads:
      if len(TOPROCESS)<=0:
        time.wait(1)
        continue

      
      print('creating thread..')
      url = TOPROCESS.pop(0)
      print(' link is = ',url)
      curthreads +=1
      
      potokname = progUID+'-'+str(potokN)
      potok = threading.Thread(target=ScanAlso, args=(url, sitename, potokname,)  )
      THREADS.put(potok)
      potok.start()
      print('inited thread ',potokname)

      potokN+=1

  print('INITED ALL')

 
  
  while (len(TOPROCESS)>0) :
        link=TOPROCESS.pop(0)
        key = link
        status = FOUNDS[key]
         
        
        #print(str(status) + ' = '+ link)
        if status == IN_STOCK:
            FOUNDS[key]= IN_PROCESSING
            try:
                ScanAlso(link, sitename)
            except:
                ERRSKIPPED +=1
                continue
            FOUNDS[key]= IN_DONELIST
            PROCESSED +=1
        print(str(PROCESSED)+'/'+str(TOTAL) + ' #E! = '+str(ERRSKIPPED)+'(DD='+str(DUPLICATES)+')')
        #input('...')
  return True    

 



 


Do() 
















