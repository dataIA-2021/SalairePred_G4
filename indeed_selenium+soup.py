from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd

header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
main_url= 'https://fr.indeed.com/jobs?q={}&l={}&sort=date&limit=50&radius=25&start={}'
base_link="https://fr.indeed.com"
s=Service('C:/Users/Tim_secure/Downloads/geckodriver.exe')
driver = webdriver.Firefox(service=s, options=Options())

def get_href(main_url,poste,lieu):
    href_list=[]
    for start in range(0,50,50):
        url=main_url.format(poste,lieu,start)
        driver.get(url) 
        driver.implicitly_wait(10)
        for job in driver.find_elements(By.ID, 'pageContent'):
            html_result=job.get_attribute('innerHTML')
            soup= BeautifulSoup(html_result,'html.parser')
            for i in soup.find_all('a'):
                # if tag has attribute of class
                if i.has_attr( "href" ):
                    k=i['href']
                    href_list.append(base_link+k)
    
    return href_list

def get_job_links(href_list):
    job_links=[]
    for a in href_list:
        if a.find('/rc/clk')!=-1:
            job_links.append(a)
        elif a.find('/company/')!=-1:
            job_links.append(a)
    return job_links

def get_job_df(job_links, lieu):
    df=pd.DataFrame(columns=["metier", "entreprise", "localisation", "avis",
                             "salaire", "contrat", "description"])
    
    for i in job_links:
        req=requests.get(i,headers=header)
        soup_req=BeautifulSoup(req.text,"html.parser")
        try:
            title=soup_req.find('h1',{'class': 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title'}).text
        except:
            continue
        try:
            company=soup_req.find('div',{'class':'icl-u-lg-mr--sm icl-u-xs-mr--xs'}).text
        except:
            continue
        for rat in soup_req.find_all('meta', {'itemprop': 'ratingValue'}):     
            try:
                rating=rat.find('content')[1].text.replace('\n', '').strip()
            except:
                continue
        try:
            location=soup_req.find('div',{'class':'jobsearch-jobLocationHeader-location'}).text
        except:
            location=lieu
        try:
            salary=soup_req.find('span', {'class' : 'icl-u-xs-mr--xs attribute_snippet'}).text
        except:
                continue
        try:
            contract=soup_req.find('span', {'class' : 'jobsearch-JobMetadataHeader-item  icl-u-xs-mt--xs'}).text
        except:
                continue
        try:
            desc=soup_req.find('div',{'class':'jobsearch-jobDescriptionText'}).text
        except:
            continue
        df = df.append({"metier":title, "entreprise":company, "avis":rating, "localisation": location, "salaire": salary, "contrat":contract, "description":desc},
                       ignore_index=True)
    
    return df

def get_poste(main_url,poste,lieu):
    
    href_list= get_href(main_url,poste,lieu)
    
    job_links= get_job_links(href_list)
    
    job_df= get_job_df(job_links,lieu)
    
    return job_df

data_df= get_poste(main_url,poste='data',lieu='France')