import subprocess

def ipSearch():
    
    cmd = 'arp -a | findstr "e0-e2-e6-aa-84-a4"'
    returned_output = subprocess.check_output((cmd),shell=True,stderr=subprocess.STDOUT)
    # print(returned_output)
    parse=str(returned_output).split(' ',1)
    ip=parse[1].split(' ')
    # print(ip[1])
    # print(type(ip[1]))

    url ="http://"+ip[1]+"/capture?_cb=1656024603205"
    print(type(url))
    return(url)
