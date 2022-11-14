def spot():
    cnt = 0
    ig = 0
    client_id = ''
    client_secret = ''
    with open('data\\cred\\cred.sec', 'r') as file:
        data = file.read().split('\n')
        for i in data:
            cnt+=1
            if cnt == 1:
                for j in i:
                    ig+=ord(j)
                    ig+=11231231
            else:
                txt = ''
                for j in i.split('\\'):
                    if j:
                        txt+=chr(int(j)-ig)
                if cnt == 2:
                    client_id = txt
                elif cnt == 3:
                    client_secret = txt
    return client_id, client_secret
