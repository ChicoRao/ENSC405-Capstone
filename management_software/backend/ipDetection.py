import subprocess

def ipSearch():
    try:
        macList = ['0c-b8-15-f4-9f-38','ec-62-60-9a-8d-a0']
        urlList = []
        for item in macList:
            cmd = 'arp -a | findstr ' + item
            returned_output = subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT)
            # print('print return output', returned_output)
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



