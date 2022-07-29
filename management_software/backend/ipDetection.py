import subprocess

def ipSearch():
    try:
        macList = ['0c-b8-15-c4-e0-f8', 'e0-e2-e6-aa-84-a4']
        urlList = []
        for item in macList:
            cmd = 'arp -a | findstr ' + item
            returned_output = subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT)
                # print(returned_output)
            parse=str(returned_output).split(' ',1)
            ip=parse[1].split(' ')
            # print(ip[1])
            # print(type(ip[1]))
            url ="http://"+ip[1]+"/capture?_cb=1656024603205"
            urlList.append(url)
            print(type(url))
            print (url)
        
    except:
            
        url = ' '   
        print("No camera connected")
            
    finally:
        print(urlList)
        return (urlList)



