import os
import urllib.request
import urllib.parse
import threading
import queue
import time 
import random


'''Here is the parameter setting'''
q=queue.Queue()
threading_num=5
domain_name="http://www.tku.edu.tw/"
Baidu_Spider="Mozilla 6.0"
Charset="UTF-8"
Queue_num=0
result_list=[]




'''Here work with dictionarty modules!'''
exclude_list=['.jpg','.gif','.css','.png','.js']
with open ("doc.txt","r") as lines:
    for line in lines:
        line=line.rstrip()
        if os.path.splitext(line)[1] not in exclude_list:
            Queue_num+=1
            q.put(line)
print("There are %s path in the list" %(Queue_num))
print("type any world to continue")
input()


'''Thead used main function!'''            
def crawler():
    while not q.empty():
        path=q.get()
        url="%s%s" %(domain_name,path)
        opener=urllib.request.build_opener()
        urllib.request.install_opener(opener)
        headers={}
        headers['User-Agent']=Baidu_Spider
        headers['Content-Type']=Charset
        data=urllib.parse.urlencode(headers)

#This is fuckint binary data encoding
        bData=data.encode('ascii')
        request=urllib.request.Request(url,bData)
        try:
            response=urllib.request.urlopen(request)
            content=response.read()
            if len(content):
                finalurl = response.geturl()
                if finalurl!=url:
                    print("Detect redirectrion by server!")
                    print ("We are in %s now"%(finalurl))
                    #print("States[%s]:Path:%s" % (str(response.getcode()), url))
                else:
                    result_list.append(url)
                    print("States[%s]:Path:%s" %(str(response.getcode(),url)))
        except urllib.error.HTTPError as e:
            print ("Get error in HTTP connection")


def print_result():
    for list in result_list:
        print(list)


if __name__=="__main__":
    print("Program is start!")
    for i in range(threading_num):
        t=threading.Thread(target=crawler)
        t.start()
        print_result()



