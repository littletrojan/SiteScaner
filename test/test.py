#!python3

import os
import urllib.request
import urllib.parse
import threading
import queue
import time 
import random
from optparse import OptionParser
import sys
import progressbar
'''Here is about the optionalparser '''
usage = "usage: %prog [options] arg1 arg2"
parser=OptionParser(usage=usage)

#Thread number setting parser
parser.add_option("-t","--thread",dest="thread_num",type="int",help="Open thread number(optional)",default="1")

#Target name setting parser
parser.add_option("-u","--url",dest="url",type="string",help="Target url to scan(required)")

#Show detail message setting parser
parser.add_option("-v",dest="show_message",action="store_true",default=False,help="Set this argument to show the detail(optional)")

#define dictionary setting parser,default using doc.txt whitch content more than 40000 list of path.
parser.add_option("-d","--dict",dest="dictionary",metavar="FILE",default="doc.txt")

#define the execlution name in the dictionary want to exclude
parser.add_option("-e","--execlude",dest="exclude_list",action="append",help="Setting the excludtion extend file name whitch you don't want to try,like .jpg .gif etc")

exclude_list=['.jpg','.gif','.css','.png','.js']
   

class HTTPBackendScanner(object):
    
    result_list=[]
    Baidu_Spider=""
    Charset=""
    def __init__(self,local_threading_num,local_domain_name,local_showdetail,local_excludelist,local_dictionary): 
        self.threading_num=local_threading_num
        self.domain_name=local_domain_name
        self.UserAgent="Mollize6.0"
        self.Charsetr="UTF8"
        self.showdetail=local_showdetail
        self.excludelist=local_excludelist
        self.q=queue.Queue()
        self.Queue_num=0
        self.dictionary=local_dictionary
    
    '''
    Before starting the crawler we should parse the dictionary,and exclude the file we don't really want,
    and put it in to the queue in the end.
    '''
    def DictParser(self):
        print("Starting to parse dictionary line by line...")
        with open (dictionary,"r") as lines:
            for line in lines:
                line=line.rstrip()
                if os.path.splitext(line)[1] not in exclude_list:
                    self.Queue_num+=1
                    self.q.put(line)
            print("There are %s path in the list" %(self.Queue_num))
            

    def crawler(self):
        HttpStatus=''
        print("thread %s  strart "% (str(threading.get_ident())))
        while not self.q.empty():
            path=self.q.get()
            url="%s%s" %(domain_name,path)
            opener=urllib.request.build_opener()
            urllib.request.install_opener(opener)
            headers={}
            headers['User-Agent']=self.Baidu_Spider
            headers['Content-Type']=self.Charset
            data=urllib.parse.urlencode(headers)
            bData=data.encode('ascii')
            request=urllib.request.Request(url,bData)

            try:
                print("Try to connecting %s"%(url),end='\t')                    #We dont want it to change line print.
                response=urllib.request.urlopen(request)
                content=response.read()
                if len(content):
                    finalurl = response.geturl()
                    if finalurl!=url:
                        if self.showdetail:
                            print("Detect redirectrion by server! We are in %s now"  %(finalurl))
                        else:
                            print("{0}".format("303 Redirection"))
                    #print(threading.Thread.getname())
                    #print("States[%s]:Path:%s" % (str(response.getcode()), url))
                    else:
                        result_list.append(url)
                        print("States[%s]:Path:%s" %(str(response.getcode(),url)))
            except urllib.error.HTTPError as e:
                if self.showdetail:
                    print ("Get error in HTTP connection",end ="")
                    print(e.getreason)
                    if self.HttpErrorHandler(e.getreason):
                        pass
                else:
                    if self.HttpErrorHandler(e.getreason):
                        continue
                    else:
                        sys.exit(1)
    def HttpErrorHandler(self,errstr):
        if errstr=="not found":                                                     #If http error is 404 not found
            return True
        else:
            return False
        

    
    def print_result(self):
        for list in  self.result_list:
            print(list)

    '''
    After HttpBackenScan start all work will use thread to do.
    '''
    def starting_thread(self):
        for i in range(threading_num):
            t=threading.Thread(target=self.crawler)
            t.start()
            self.print_result()
    '''
    Scaner's main logic  function
    '''
    def run(self):
        self.starting_thread()
        self.print_result()



if __name__=="__main__":
    (option,args)=parser.parse_args()
    if (option.url==None):                              #if user pass none url.
        parser.print_help()
        exit(1)
        
    print("Program is start!")
    print(option.url)
    threading_num=option.thread_num                     #specified the thread numbers.
    domain_name=option.url+"/"                          #Modify url so that it can be strcat with another file path
    print(i"Going to parsing url:"+domain_name+"\n")          #print url after it has benn modify.
    userinput=input("Type any word to continue...or type quit to quit.,type help to get help")
    if userinput.lower()=="quit":
        print("byebye")
        sys.exit(0)
    else:
        paser.print_help()
           
    showdetail=option.show_message                      #Show the detail or not
    excludelist=exclude_list
    dictionary=option.dictionary
    scanner=HTTPBackendScanner(threading_num,domain_name,showdetail,excludelist,dictionary)
    scanner.DictParser()
    scanner.run()


