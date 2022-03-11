import pandas as pd
import re
import numpy as np
import string

df_11=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_11.csv')

df_24=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_24.csv')

df_27=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_27.csv')

df_28=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_28.csv')

df_32=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_32.csv')

df_44=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_44.csv')

df_52=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_52.csv')

df_75=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_75.csv')

df_76=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_76.csv')

df_84=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_84.csv')

df_93=pd.read_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\data_93.csv')

df_indeed = pd.read_csv('C:\\Users\Tim_secure\\Documents\\Projet Greta\\data_indeed.csv')
df_indeed.drop(['Unnamed: 0','Rating'], axis=1, inplace=True)
df_indeed2 = df_indeed[df_indeed.Salary != 'None'].drop_duplicates().dropna()
df_indeed2_=df_indeed2.copy()
def salary_stripper(dataframe, column):
    dataframe[str(column)] = dataframe[str(column)].replace({'\€':'', ',': '.'}, regex = True)
    dataframe[str(column)].replace(regex=True,inplace=True,to_replace=r'\D',value=r' ')
    dataframe[str(column)] = dataframe[str(column)].str.replace(' ',',')
    dataframe = dataframe.join(dataframe[str(column)].str.split(',,,', 1, expand=True).rename(columns={0:'Low', 1:'High'}))
    dataframe['Low'] = dataframe['Low'].str.replace(',','')
    dataframe['Low'] = dataframe['Low'].astype('float64')
    dataframe.drop(str(column), axis=1, inplace=True)
    dataframe['High'] = dataframe['High'].str.replace(',','')
    dataframe['High'] = dataframe['High'].apply(pd.to_numeric)
    dataframe['Average'] = dataframe[['Low', 'High']].mean(axis=1)
    return dataframe

df_indeed = salary_stripper(df_indeed2_, 'Salary')
extracted_col = df_indeed["Average"]
df_indeed2=df_indeed2.join(extracted_col)

df_indeed2["Average"]=np.where(df_indeed2["Salary"].str.contains('mois'), df_indeed2["Average"]*12, df_indeed2["Average"])
df_indeed2["Average"]=np.where(df_indeed2["Salary"].str.contains('heure'), df_indeed2["Average"]*35*52.143, df_indeed2["Average"])
df_indeed2["Average"]=np.where(df_indeed2["Salary"].str.contains('18,86 € par heure'), 18.86*35*52.143, df_indeed2["Average"])
df_indeed2["Average"]=np.where(df_indeed2['Salary'].str.contains('semaine'), df_indeed2["Average"]*52.143, df_indeed2["Average"])

df_indeed2.rename(columns={'Title':'intitule', 'Location':'lieuTravail.libelle', 'Company':'entreprise.nom', 'Synopsis':'description'}, inplace=True)

df_adaptif=pd.concat([df_11, df_24,df_27, df_28, df_32, df_44, df_52, df_75, df_76, df_84, df_93, df_indeed2])

#df_adaptif.to_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\pôle_emploi_indeed.csv')

df_adaptif=df_adaptif.dropna(subset=['salaire.libelle', 'Average', 'salaire.commentaire','salaire.complement1', 'salaire.complement2'], how='all')

df_adaptif=df_adaptif.drop(['id', 'Unnamed: 0', 'dateCreation', 'dateActualisation', 'accessibleTH', 'entreprise.entrepriseAdaptee', 'contact.nom', 
                          'contact.coordonnees1','agence.courriel','contact.commentaire', 'contact.urlPostulation', 'permis', 
                          'experienceCommentaire','entreprise.logo', 'lieuTravail.latitude', 'lieuTravail.longitude',
                          'entreprise.url', 'nombrePostes', 'deplacementCode',
                          'deplacementLibelle', 'offresManqueCandidats', 'alternance', 'contact.courriel',
                          'origineOffre.origine', 'origineOffre.urlOrigine', 'complementExercice', 
                          'origineOffre.partenaires', 'contact.coordonnees3'],axis=1)


df_adaptif['salaire.libelle'] = df_adaptif['salaire.libelle'].fillna(df_adaptif['salaire.commentaire'])
df_adaptif= df_adaptif.applymap(lambda s:s.lower() if type(s) == str else s)
remove_words = ['A négocier', 'De', 'FD', 'compétitif', 'SELON LA GRILLE DE FHF', 'selon profil', 'Selon grille FPH', 'Fixe + variable', 'Selon convention FNCL', 'Selon profil', 'Selon expérience', 'A définir selon profil', 'suivant grille indiciaire FPH', 
                'Varie selon', 'Selon le profit d', 'fixe + variable','12 mois + prime décentralisée', 'à négocier', 'Interessement', 'A partirr de', 'Selon le profil d']
pat = r'\b(?:{})\b'.format('|'.join(remove_words))
df_adaptif['salaire.libelle'] = df_adaptif['salaire.libelle'].str.replace(pat, '')
df_adaptif=df_adaptif.drop(['salaire.commentaire'],axis=1)


df_adaptif= df_adaptif.applymap(lambda s:s.lower() if type(s) == str else s)

df_adaptif['salaire.libelle']=np.where(df_adaptif[['salaire.libelle']].apply(lambda x: x.str.contains('prime décentralisée', case=False, regex=True)).any(1), None, df_adaptif['salaire.libelle'])
                                                                              

df_adaptif['poste'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description']].apply(lambda x: x.str.contains('big data')).any(1), 'developpeur big data', None)
df_adaptif['data_scientist']=np.where(df_adaptif[['intitule', 'appellationlibelle', 'description']].apply(lambda x: x.str.contains('data scientist')).any(1), 'data scientist', None)
df_adaptif['data_analyst'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description']].apply(lambda x: x.str.contains('data analyst|analyste|développeur data', case=False, regex=True)).any(1), 'data analyst', None)
df_adaptif['data_manager'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description']].apply(lambda x: x.str.contains('data manager|chief|chef|leader|gouvernance', case=False, regex=True)).any(1), 'data manager', None)
df_adaptif['consultant'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description']].apply(lambda x: x.str.contains('consultant|bi|business intelligence', case=False, regex=True)).any(1), 'consultant data', None)
df_adaptif['data engineer'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description']].apply(lambda x: x.str.contains('data engineer|ingénieur data|architecte|architect',
                                                 case=False, regex=True)).any(1), 'data engineer', None)


df_adaptif=df_adaptif.dropna(subset=['data_scientist', 'data_analyst','poste', 'data_manager', 'consultant',  
                                    'data engineer'], how='all')
df_adaptif['poste'] = df_adaptif['poste'].fillna(df_adaptif['data_analyst'])
df_adaptif['poste'] = df_adaptif['poste'].fillna(df_adaptif['data_scientist'])
df_adaptif['poste'] = df_adaptif['poste'].fillna(df_adaptif['data engineer'])
df_adaptif['poste'] = df_adaptif['poste'].fillna(df_adaptif['data_manager'])
df_adaptif['poste'] = df_adaptif['poste'].fillna(df_adaptif['consultant'])



df_adaptif=df_adaptif.drop(['data_scientist',
                          'data_analyst','data_manager','data engineer', 
                          'consultant',],axis=1)

df_adaptif['bac+'] = df_adaptif['formations'].str.extract('([a-zA-Z+]+[0-9-])',expand= True)

df_adaptif['bac+1']=df_adaptif['description'].str.extract('(\+[0-9.])',expand= True)
df_adaptif['bac+1'] = np.where(df_adaptif[['intitule', 'description',
                                            'entreprise.description', 'competences']].apply(lambda x: x.str.contains('bac+',
                                                 case=False, regex=True)).any(1),df_adaptif['bac+1'] , None)
                                                                                                                     
df_adaptif['bac+1']=df_adaptif['bac+1'].str.extract("(\d+)", expand=True)                                                                                                                                                                                                       
df_adaptif['bac+']=df_adaptif['bac+'].str.extract("(\d+)", expand=True)
df_adaptif['bac+'] = df_adaptif['bac+'].astype(float)
df_adaptif['bac+1'] = df_adaptif['bac+1'].astype(float)
df_adaptif['bac+'] = df_adaptif['bac+'].fillna(df_adaptif['bac+1'])
df_adaptif['bac+']=np.where(df_adaptif[['formations']].apply(lambda x: x.str.contains('bac ou équivalent',
                                                 case=False, regex=True)).any(1), 0, df_adaptif['bac+'])


df_adaptif['dureeTravail'] = df_adaptif['dureeTravailLibelle'].str.extract("(\d+\w+? |\d+\w+?\d+)", expand=True)

df_adaptif['dureeTravail1'] = df_adaptif['dureeTravail'] .str.extract("([a-zA-Z+]+[0-9+])", expand=True)

df_adaptif['dureeTravail'] = df_adaptif['dureeTravail'].str.extract("(\d+)", expand=True)
df_adaptif['dureeTravail1']=df_adaptif['dureeTravail1'].str.extract("(\d+)", expand=True) 
df_adaptif['dureeTravail1']=(df_adaptif['dureeTravail1'].astype(float))/6
df_adaptif['dureeTravail1'] = df_adaptif['dureeTravail1'].fillna(0) 
df_adaptif['dureeTravail']=(df_adaptif['dureeTravail'].astype(float))+(df_adaptif['dureeTravail1'].astype(float))

df_adaptif['dureeTravail2'] = df_adaptif['description'].str.extract(r'(\d+.?\d*)h')
df_adaptif['dureeTravail2'] = pd.to_numeric(df_adaptif['dureeTravail2'],errors='coerce')
df_adaptif['dureeTravail2'] = np.where(df_adaptif['dureeTravail2']< 10, df_adaptif['dureeTravail2']*5, df_adaptif['dureeTravail2'])
df_adaptif['dureeTravail2'] = np.where(df_adaptif['dureeTravail']> 50, None, df_adaptif['dureeTravail'])
df_adaptif['plein'] = np.where(df_adaptif[['intitule', 
                                           'description','dureeTravailLibelleConverti',
                                           'dureeTravailLibelle']].apply(lambda x: x.str.contains('temps plein', case=False, regex=True)).any(1), 35, None)
df_adaptif['dureeTravail2']=df_adaptif['dureeTravail2'].fillna(df_adaptif['plein'])

df_adaptif['dureeTravail'] = df_adaptif['dureeTravail'].fillna(df_adaptif['dureeTravail2'])
df_adaptif['dureeTravail']=df_adaptif['dureeTravail'].round(decimals = 2) 

df_adaptif['lieuTravail.libelle']=df_adaptif['lieuTravail.libelle'].str.rstrip(string.digits)
df_adaptif['lieuTravail.libelle']=df_adaptif['lieuTravail.libelle'].replace({'nouvelle-aquitaine':'87 - limoges'})
df_adaptif['Departement']=df_adaptif['lieuTravail.libelle'].str.extract(r'(\d{2})', expand=True)
df_adaptif.isna().sum()
df_adaptif['Departement'] = df_adaptif['Departement'].fillna(df_adaptif['lieuTravail.commune'].astype(str).str[:2])
df_adaptif['Departement']=np.where(df_adaptif[['entreprise.nom']].apply(lambda x: x.str.contains('ardemis partners',
                                                 case=False, regex=True)).any(1), 13, df_adaptif['Departement'])
df_adaptif['Departement'] = df_adaptif['Departement'].astype(str)

df_adaptif['Contrat']=np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('intérim', case=False, regex=True)).any(1), 'mis', None)

df_adaptif['CDI']=np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('cdi')).any(1), 'cdi', None)
                                                                                                                   
df_adaptif['CDD']=np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('cdd')).any(1), 'cdd', None)


df_adaptif['Contrat'] = df_adaptif['Contrat'].fillna(df_adaptif['CDD'])
df_adaptif['Contrat'] = df_adaptif['Contrat'].fillna(df_adaptif['CDI'])
df_adaptif['Contrat'] = df_adaptif['Contrat'].fillna(df_adaptif['typeContrat'])
droping=['apprentissage', 'professionnalisation', 'freelance']
df_adaptif = df_adaptif[df_adaptif.Contrat.isin(droping) == False]                                              



df_adaptif['Statut'] = df_adaptif['qualificationCode']
df_adaptif['Statut']=df_adaptif['Statut'].astype(float)
df_adaptif['Statut1'] = np.where(df_adaptif['Average']>= 35000, 9, None)
df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif['Statut1'])

to_replace = {'ï¿½': '', 'à': '', 'mois': '', 'horaire': '','euros': '', 
       'annuel': '', 'autre': '', 'de': '', 'partir': '', 'a': '', 'mensuel': '',  
       'brut': '', 'sur 12.5': '', 'sur 12': '', 'sur 13.3' :'', 'sur 13': '', 'k€': '', ',00': '', ',': '.'
       }


df_adaptif['salaire'] =df_adaptif['salaire.libelle'] .replace(to_replace, regex=True)

df_adaptif['salaire'] = df_adaptif['salaire'].str.strip()

df_adaptif['salaire_min'] = df_adaptif['salaire'].str.extract('(\d+\.? |\d+\.\d+)',expand= True)
df_adaptif['salaire_min'] = df_adaptif['salaire_min'].fillna(df_adaptif['salaire'])

df_adaptif['salaire_min'] = pd.to_numeric(df_adaptif['salaire_min'],errors='coerce')

df_adaptif['salaire_max'] = df_adaptif['salaire'].str.extract('.*?([0-9.]+[0-9]+)$')

df_adaptif['salaire_max'] = pd.to_numeric(df_adaptif['salaire_max'],errors='coerce')

df_adaptif['salaire_moyen'] = df_adaptif[['salaire_min', 'salaire_max']].mean(axis=1)

df_adaptif['salaire_moyen']=np.where(df_adaptif[['salaire.libelle']].apply(lambda x: x.str.contains('mensuel')).any(1), df_adaptif['salaire_moyen']*12, df_adaptif['salaire_moyen'])

df_adaptif['salaire_moyen']=np.where(df_adaptif[['salaire.libelle']].apply(lambda x: x.str.contains('k€')).any(1), df_adaptif['salaire_moyen']*1000, df_adaptif['salaire_moyen'])

df_adaptif['salaire_moyen']=np.where(df_adaptif[['salaire.libelle']].apply(lambda x: x.str.contains('horaire')).any(1), df_adaptif['salaire_moyen']*df_adaptif['dureeTravail']*52.143, df_adaptif['salaire_moyen'])

df_adaptif['salaire_moyen']=df_adaptif['salaire_moyen'].astype(float)


df_adaptif['Average']=df_adaptif['Average'].fillna(df_adaptif['salaire_moyen'])

df_adaptif.dropna(subset = ['Average'], inplace=True)



df_adaptif['experience'] = df_adaptif['experienceLibelle'].str.extract("(\d+)", expand=True)

df_adaptif['mexperience']=df_adaptif['description'].str.extract(r'(\d+.?\d*) an')
df_adaptif['mexperience']=df_adaptif['mexperience'].str.extract("(\d+)", expand=True)
df_adaptif['mexperience']=df_adaptif['mexperience'].astype(float)
df_adaptif['mexperience'] = np.where(df_adaptif['mexperience']> 10, None, df_adaptif['mexperience'])
df_adaptif['dexperience'] = np.where(df_adaptif[['intitule', 'description', 'experienceLibelle']].apply(lambda x: x.str.contains('débutant|jeune diplômé', case=False, regex=True)).any(1), 0, None)

df_adaptif['1experience'] = np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('première expérience', case=False, regex=True)).any(1), 1, None)

df_adaptif['Sexperience'] = np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('senior|expert|experte', case=False, regex=True)).any(1), 5, None)
df_adaptif['jexperience'] = np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('junior', case=False, regex=True)).any(1), 2, None)
df_adaptif['cexperience'] = np.where(df_adaptif[['intitule', 'description']].apply(lambda x: x.str.contains('confirmé', case=False, regex=True)).any(1), 4, None)
df_adaptif['experience']=df_adaptif['experience'].fillna(df_adaptif['mexperience'])
df_adaptif['experience']=df_adaptif['experience'].fillna(df_adaptif['Sexperience'])
df_adaptif['experience']=df_adaptif['experience'].fillna(df_adaptif['cexperience'])
df_adaptif['experience']=df_adaptif['experience'].fillna(df_adaptif['dexperience'])
df_adaptif['experience']=df_adaptif['experience'].fillna(df_adaptif['jexperience'])
df_adaptif['experience']=df_adaptif['experience'].fillna(df_adaptif['1experience'])
df_adaptif['experience']=df_adaptif['experience'].astype(float)

df_adaptif=df_adaptif.drop_duplicates(subset=['poste', 'Departement', 'entreprise.nom', 'Average', 'Contrat'])
df_adaptif['experience'] = df_adaptif['experience'].fillna(df_adaptif.groupby(['Average', 'poste', 'dureeTravail', 'Contrat'])['experience'].transform('mean'))


df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif.groupby(['poste', 'Contrat', 'experience'])['Statut'].transform('mean'))
df_adaptif['Statut'] = np.where(df_adaptif['Statut']> 8, 9, df_adaptif['Statut'])
df_adaptif['Statut'] = np.where((df_adaptif['Statut']> 7) & (df_adaptif['Statut']<8), 8, df_adaptif['Statut'])
df_adaptif['Statut2'] = np.where(df_adaptif['Average']>= 35000, 9, None)
df_adaptif['Statut']=df_adaptif['Statut'].fillna(df_adaptif['Statut2'])
df_adaptif['Statut3']=np.where(df_adaptif[['Contrat']].apply(lambda x: x.str.contains('apprentissage|professionnalisation')).any(1), 6, None)
df_adaptif['Statut']=df_adaptif['Statut'].fillna(df_adaptif['Statut3'])

df_adaptif['dureeTravail']=df_adaptif['dureeTravail'].fillna(35)




df_adaptif['dureeTravail_annuelle']=df_adaptif['dureeTravail'] /5*220
df_adaptif['dureeTravail_annuelle']=df_adaptif['dureeTravail_annuelle'].astype(float)

df_adaptif['Average'] = np.where(df_adaptif[['Contrat']].apply(lambda x: x.str.contains('stage',
                                                 case=False, regex=True)).any(1), 1440*6, df_adaptif['Average'])

#df_adaptif['Average']=df_adaptif['Average'].fillna(df_adaptif.groupby(['poste', 'Contrat', 'Statut', 'experience'])['Average'].transform('mean'))
df_adaptif['bac+']=df_adaptif['bac+'].fillna(df_adaptif.groupby(['poste', 'Contrat', 'Statut'])['bac+'].transform('mean'))
df_adaptif['bac+']=df_adaptif['bac+'].fillna(df_adaptif.groupby(['poste', 'Statut'])['bac+'].transform('mean'))
df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif.groupby(['poste', 'Average'])['Statut'].transform('mean'))
df_adaptif['experience'] = df_adaptif['experience'].fillna(df_adaptif.groupby(['Average', 'poste', 'Contrat'])['experience'].transform('mean'))
df_adaptif['experience1']=np.where(df_adaptif['Average']>=60000, 5, None)
df_adaptif['experience'] = df_adaptif['experience'].fillna(df_adaptif['experience1'])
#df_adaptif['Average']=df_adaptif['Average'].fillna(df_adaptif.groupby(['poste', 'Contrat'])['Average'].transform('mean'))
df_adaptif['experience'] = df_adaptif['experience'].fillna(df_adaptif.groupby(['Average', 'poste', 'Contrat'])['experience'].transform('mean'))
df_adaptif['bac+']=df_adaptif['bac+'].fillna(df_adaptif.groupby(['poste', 'Average'])['bac+'].transform('mean'))
df_adaptif['bac+']=df_adaptif['bac+'].fillna(df_adaptif.groupby(['poste', 'experience'])['bac+'].transform('mean'))
df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif.groupby(['Contrat', 'bac+'])['Statut'].transform('mean'))
df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif.groupby(['poste', 'Average'])['Statut'].transform('mean'))
df_adaptif['experience'] = df_adaptif['experience'].fillna(df_adaptif.groupby(['bac+', 'Contrat'])['experience'].transform('mean'))
df_adaptif['experience'] = df_adaptif['experience'].astype(float)
df_adaptif.rename(columns={'Average': 'Salaire_Annuel'}, inplace=True)
df_adaptif['bac+']=df_adaptif['bac+'].fillna(df_adaptif.groupby(['Salaire_Annuel', 'dureeTravail_annuelle'])['bac+'].transform('mean'))
df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif.groupby(['Salaire_Annuel', 'dureeTravail_annuelle','Contrat'])['Statut'].transform('mean'))
df_adaptif['Statut'] = df_adaptif['Statut'].fillna(df_adaptif.groupby(['dureeTravail_annuelle','poste'])['Statut'].transform('median'))
df_adaptif['bac+']=df_adaptif['bac+'].fillna(df_adaptif.groupby(['Statut', 'dureeTravail_annuelle'])['bac+'].transform('mean'))
df_adaptif['Statut'] = df_adaptif['Statut'].round()
df_adaptif['bac+']=df_adaptif['bac+'].round()



                                                
df_adaptif=df_adaptif.drop(['salaire_min','salaire_max','Statut1', 'Statut2', 'CDD', 'plein','mexperience','cexperience', 
                           'salaire', 'CDI','Statut3','dureeTravail1','Sexperience','dexperience',
                           'dureeTravail2','bac+1','salaire_moyen', 'jexperience','1experience', 'experience1',
                           'dureeTravail'],axis=1)


df_adaptif['langages_programmation'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description',
                                            'entreprise.description', 'competences']].apply(lambda x: x.str.contains('python|java|flutter|.net|julia|rstudio|matlab|scala|sas',
                                                 case=False, regex=True)).any(1), 1, 0)

                                                                                                                  
df_adaptif['langages_Web'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description',
                                            'entreprise.description', 'competences']].apply(lambda x: x.str.contains('javascript|php|css|html',
                                                 case=False, regex=True)).any(1), 1, 0)


df_adaptif['bases_donnees'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description',
                                            'entreprise.description', 'competences']].apply(lambda x: x.str.contains('sql|postgresql|mysql|nosql|mongodb',
                                                 case=False, regex=True)).any(1), 1, 0)                                                                                                                     

                                                                                                                    
df_adaptif['BI_soft'] = np.where(df_adaptif[['intitule', 'appellationlibelle', 'description',
                                            'entreprise.description', 'competences']].apply(lambda x: x.str.contains('powerbi|power bi|tableau|sisense|qlik|sisense|analytics',
                                                 case=False, regex=True)).any(1), 1, 0)

                                                                                                                     
df_adaptif['Anglais']=np.where(df_adaptif[['langues', 'description']].apply(lambda x: x.str.contains('anglais|english', case=False, regex=True)).any(1), 1, 0)                                                                                                                    


new_df = df_adaptif.filter(['poste', 'Departement', 
                            'experience','Contrat', 'Statut', 'dureeTravail_annuelle',
                            'bac+', 'Anglais',
                            'langages_programmation',
                            'langages_Web',
                            'bases_donnees', 'BI_soft',
                            'Salaire_Annuel'], axis=1)                                                                                                                         
new_df.isna().sum()                                                                                                                     #df_adaptif.info()
new_df.to_csv('C:\\Users\\Tim_secure\\Documents\\GitHub\\test\\preprocessing_emploi.csv')
