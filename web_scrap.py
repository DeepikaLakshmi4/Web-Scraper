from nturl2path import url2pathname
from click import style
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import os

def extract(page):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url= f'https://www.proeves.com/karnataka/bangalore/whitefield/preschool-in-whitefield-bangalore/{page}'
    r = requests.get(url,headers)
    s=BeautifulSoup(r.content,'html.parser')
    return s

def inside(link):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    url = link 
    r = requests.get(url,headers)
    s= BeautifulSoup(r.content,'html.parser')

    divs = s.find_all('div', class_ ='col-lg-12 contactDetail')

    for item in divs: 
        for tag in item.find_all('span', class_='review'):
            tag.decompose() 
        
        #coordinator
        spans= (item.span)
        coordinator = str(spans.text)[4:]

        #contact
        next = spans.find_next_siblings("span")
        contact = str(next[0].text)[4:]

        #mail 
        for tag in item.find_all('p', attrs={'class':'mb-3'}):
            tag.decompose() 
        
        for tag in item.find_all('p', attrs={'class':'allDis'}):
            tag.decompose()

        mail= item.p
        mail_ = (mail.text[4:])

        #website
        website = mail.find_next_siblings("p")
        try:
            website = (website[0].text)[3:]
            #print(website)
        except: 
            #print("none")
            website = "None"


        return [coordinator, contact, mail_, website]
        




def transform(s):
    divs = s.find_all('div', class_ ='col-lg-6')
    for item in divs:
        
        #title
        title = item.find('a').text.strip()

        #address
        addres = item.find('address')
        y=str(addres)
        
        if(len(str(title))>1):

            name = title

            if(y!='None'):
                end=y.rfind('<')
                start=y[0:end].rfind('>')
                address=y[(start+1):end]
                
                link=item.find('a' , class_ = 'btn btn-primary rounded text-white')
                link=link.get('href')
                if link.startswith("https://www.proeves.com/karnataka/bangalore/whitefield/preschool-whitefield/"):
                    details = inside(link)
                    #print(details)
        


            schools={ 
                'Name' : name ,
                'Address' : address,
                'coordinator' : details[0],
                'Contact' : details[1], 
                'Mail' : details[2],
                'Website' : details[3]
            }
            list_of_school.append(schools)
    return 






list_of_school=[]

for i in range(1,4 ):
    print(f'getting page, {i}')
    c= extract(i)
    transform(c) 

    #print(*list_of_school)
df=pd.DataFrame(list_of_school)
df.to_csv('schools.csv')
#df.to_csv("C:\Users\Deepika Lakshmi\OneDrive\Desktop\web_scrap1\schools.csv")
