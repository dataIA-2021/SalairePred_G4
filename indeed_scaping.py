import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'}
main_url = 'https://fr.indeed.com/jobs?q=data&l=France&sort=date&limit=50&radius=25&start={}'
i = 0
results = []
df_more = pd.DataFrame(
    columns=["Title", "Location", "Company", "Rating", "Salary", "Synopsis"])

for start in range(0, 3000, 50):
    sleep(0.3)
    # Grab the results from the request (as above)
    url = main_url.format(start)
    # Append to the full set of results
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    for each in soup.find_all(class_="result"):

        try:
            title = each.find('span', title=True).text.replace('\n', '')
        except:
            title = 'None'
        try:
            location = each.find(
                'div', {'class': "companyLocation"}).text.replace('\n', '')
        except:
            location = 'None'
        try:
            company = each.find(class_='companyName').text.replace('\n', '')
        except:
            company = 'None'
        try:
            salary = each.find('div', {'class': 'salary-snippet'}).text
        except:
            salary = 'None'
        try:
            rating_span = each.find('span', attrs={'class':  'ratingNumber'})
            rating = float(rating_span.text.strip().replace(',', '.'))
        except:
            rating = 'None'
        try:
            if each.find('a', href=True):

                jk = each['data-jk']
                url = 'https://fr.indeed.com/voir-emploi?jk='+(jk)
                # print(url)

                job_response = requests.get(url)
                job_soup = BeautifulSoup(job_response.content, 'html.parser')
                synopsis = job_soup.find(
                    'div', {'class': 'jobsearch-jobDescriptionText'}).text
        except:
            synopsis = None
        df_more = df_more.append({'Title': title, 'Location': location, 'Company': company,
                                 'Rating': rating, 'Salary': salary, 'Synopsis': synopsis}, ignore_index=True)
        i += 1
        if i % 100 == 0:  # Ram helped me build this counter to see how many. You can visibly see Ram's vernacular in the print statements.
            print('You have ' + str(i) + ' results. ' +
                  str(df_more.dropna().drop_duplicates().shape[0]) + " of these aren't rubbish.")
df_more.to_csv('C:\\Users\Tim_secure\\Documents\\Projet Greta\\data_indeed.csv')
