from django.shortcuts import render

import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup
items=["","","",""]
def scrap2(url):
    image=""
    name=""
    year=""
    rate=""
    session = requests.Session()
    content =session.get(url,verify=False).content
    session.headers = {"User-agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
    soup=BeautifulSoup(content, "html.parser")
    rating=soup.find_all('span',{'itemprop':'ratingValue'})
    title=soup.find_all('h1',{'class':''})
    img=soup.find_all('div',{'class':'poster'})
    t=str(title)[14:]
    counter=0
    flag=False
    for i in range(len(t)):
        if t[i]=='<' or flag:
            flag=True
            if t[i]=='>':
                counter+=1
            if counter==2:
                year+=t[i]
        if not flag:
            name+=t[i]
    r=str(rating)[30:]
    year=year[1:5]
    for i in r:
        if i=="<":
            break
        rate+=i
    if len(img)>0:
        image=img[0].find('img',{})['src']
    items[0]=name
    items[1]=rate
    items[2]=year
    items[3]=image

def scrap(url,text):
    found=False
    session = requests.Session()
    session.headers = {"User-agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
    content =session.get(url,verify=False).content
    soup=BeautifulSoup(content, "html.parser")
    tables=soup.find_all('tr',{'class':'findResult'})
    for i in tables:
        if len(i.find_all())>2:
            link = i.find_all('a')[1]
        str_link = str(link)[9:]
        s=""
        for i in str_link:
            if i=='"':
                break
            s+=i
        s="https://www.imdb.com/"+s
        scrap2(s);
        if(text.lower().strip()==items[0].lower().strip()):
            found=True
            break;
    if not found:
        items[0]=""

def applook(request):
    if request.method == 'POST':
        text = request.POST['textfield']
        url='https://www.imdb.com/find?q={}'.format(text)
        scrap(url,text)
        return render(request, 'result.html',{'name':items[0],'rate':items[1],'year':items[2],'image':items[3]})
    return render(request,'front-page.html',{})
