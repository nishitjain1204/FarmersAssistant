from utils.disease import disease_dic
import json
req = {}
for a in disease_dic:
    print(a)
    req[a]={}
    
    
    dataset = [el.strip() for el in disease_dic[a].split('<br/>')]
    temp=[]

    for data in dataset:
        if data or len(data)>1:
            temp.append(data)

    if 'healthy' in a:
        print('plant healthy')
        req[a]['status']='healthy'
        req[a]['Crop']=temp[0].split(':')[1].strip()
    else:
        req[a]['Crop']=temp[0].split(':')[1].strip()
        req[a]['status'] = 'affected'
    
        for i in range(len(temp)):
            if i==0:
                req[a]['Crop']=temp[i].split(':')[1].strip()
            if i==1:
                req[a]['Disease']=temp[i].split(':')[1].strip()
            if i==2 :
                if temp[i]!='Cause of disease:':
                    req[a]['Disease-Summary'] = temp[i]
                    i+=2
                else:
                    req[a]['Disease-Summary'] = None
                    i+=1
                req[a]['Cause']=[]
                while temp[i]!='How to prevent/cure the disease' and i<len(temp)-1:
                    req[a]['Cause'].append(temp[i])
                    i+=1
                # print(req[a]['Cause'])
                req[a]['Cure']=temp[i+1:]

# print(req)
with open("sample.json", "w") as outfile:
    json.dump(req, outfile)
            



    

   
    





    





