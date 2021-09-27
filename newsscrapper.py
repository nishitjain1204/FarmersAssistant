
from bs4 import BeautifulSoup
import json
import requests



url = "https://www.ndtv.com/page/topic-load-more?type=news&query=agriculture"

html = requests.get(url)
links = []
soup = BeautifulSoup(html.text, 'lxml')

for a in soup.find_all('a', href=True,title=True):
    links.append(a['href'])


images=[]
for img in soup.find_all('img',class_='img_brd marr10'):
    images.append(img['src'])
  
# print(images)

summary = []
for div in soup.find_all('div',class_ = 'src_itm-txt'):
    summary.append(div.string.strip())
# print(summary)

json_dict = {}
for i in range(len(links)):
    json_dict[i]={}
    # print('link : ',links[i])
    json_dict[i]['link']=links[i]
    # print('image : ',images[i])
    json_dict[i]['image'] = images[i]
    # print('summary : ',summary[i])
    json_dict[i]['summary']= summary[i]
    # print()

# print(json_dict)
json_object = json.dumps(json_dict, indent = 4) 
print(json_object)



   