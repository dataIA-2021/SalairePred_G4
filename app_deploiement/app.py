import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
import re

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


class PreprocessJob():
    ListDB = ['sql', 'postgresql', 'mysql', 'nosq', 'mongodb']
    ListLangProg = ['python', 'java', 'flutter', 'julia', 'rstudio', 'scala', 'sas', 'c++']
    ListLangWeb = ['javascript', 'php', 'css', 'html']
    ListBI = ['powerbi', 'power bi', 'tableau', 'sisense', 'qlik', 'sisense', 'analytics']

    def __init__(self, df):

        self.df_ = df

        self.df_['Description'] = self.df_['Description'].apply(self.text_cleaning_encoding)

        self.df_['statut'] = self.df_['metier'].map(self.isStatut)
        self.df_['dureTravail'] = self.df_['contrat'].map(self.isDureT)

        self.df_['bac+'] = self.df_['metier'].map(self.isBac)
        self.df_['Anglais'] = self.df_['Description'].map(self.isAnglais)
        self.df_['LangProg'] = self.df_['Description'].map(self.isLangProg)
        self.df_['LangWeb'] = self.df_['Description'].map(self.isLangWeb)
        self.df_['BD'] = self.df_['Description'].map(self.isDB)
        self.df_['BI_soft'] = self.df_['Description'].map(self.isBI_soft)
        self.df_['DataScientist'] = self.df_['metier'].map(self.isDataScientist)
        self.df_['DataManager'] = self.df_['metier'].map(self.isDataManager)
        self.df_['DevBigData'] = self.df_['metier'].map(self.isDevBigData)
        self.df_['DataEngineer'] = self.df_['metier'].map(self.isDataEngineer)
        self.df_['DataAnalyst'] = self.df_['metier'].map(self.isDataAnalyst)
        self.df_['CDI'] = self.df_['contrat'].map(self.isCDI)
        self.df_['CDD'] = self.df_['contrat'].map(self.isCDD)
        self.df_['Intérim'] = self.df_['contrat'].map(self.isInterim)

        self.X = self.df_.drop(columns=['metier', 'contrat', 'Description'])
        # self.y = self.df_['Salaire']

    def text_cleaning_encoding(self, text):
        text = text.lower()  # Converting text into lowercase
        text = re.sub('h/f', '', text)  # Removing h/f
        text = re.sub('\(', '', text)  # Removing )
        text = re.sub('\)', '', text)  # Removing (
        text = re.sub('f/h', '', text)  # Removing f/h
        text = re.sub('it', '', text)  # Removing it
        text = re.sub("\n", '', text)  # Removing new lines
        return (text)

    def isCDI(self, txt):
        if bool(re.search("CDI", txt)):
            return 1
        else:
            return 0

    def isCDD(self, txt):
        if bool(re.search("CDD", txt)):
            return 1
        else:
            return 0

    def isInterim(self, txt):
        if bool(re.search("Interim", txt)):
            return 1
        else:
            return 0

    def isDataScientist(self, txt):
        if bool(re.search("(?=.*scientist)(?=.*data)", txt)):
            return 1
        else:
            return 0

    def isDataAnalyst(self, txt):
        if bool(re.search("(?=.*Data)(?=.*Analyst)", txt)):
            return 1
        else:
            return 0

    def isDataEngineer(self, txt):
        if bool(re.search("(?=.*Data)(?=.*Engineer)", txt)):
            return 1
        else:
            return 0

    def isDataManager(self, txt):
        if bool(re.search("(?=.*Data)(?=.*Manager)", txt)):
            return 1
        else:
            return 0

    def isDevBigData(self, txt):
        if bool(re.search("(?=.*Developpeur)(?=.*BigData)", txt)):
            return 1
        else:
            return 0

    def isAnglais(self, txt):
        if bool(re.search("(?=.*anglais)", txt)):
            return 1
        else:
            return 0

    def isLangProg(self, txt):
        for PreprocessJob.ListLangProg in txt:
            return 1
        else:
            return 0

    def isLangWeb(self, txt):
        for PreprocessJob.ListLangWeb in txt:
            return 1
        else:
            return 0

    def isDB(self, txt):
        for PreprocessJob.ListDB in txt:
            return 1
        else:
            return 0

    def isBI_soft(self, txt):
        for PreprocessJob.ListBI in txt:
            return 1
        else:
            return 0

    def isBac(self, txt):
        if txt == 'Developpeur BigData':
            return 5
        elif txt == "Data Scientist":
            return 5
        elif txt == "Data Analyst":
            return 4
        elif txt == "Data Engineer":
            return 5
        elif txt == "Data Manager":
            return 3

    def isStatut(self, txt):
        if txt == 'Developpeur BigData':
            return 9
        elif txt == "Data Scientist":
            return 9
        elif txt == "Data Analyst":
            return 7
        elif txt == "Data Engineer":
            return 9
        elif txt == "Data Manager":
            return 8

    def isDureT(self, txt):
        if txt == 'CDI':
            return 1540
        else:
            return 1606

    def isPython(self, txt):
        if bool(re.search("python", txt)):
            return 1
        else:
            return 0

    def isJava(self, txt):
        if bool(re.search("java", txt)):
            return 1
        else:
            return 0

    def isSql(self, txt):
        if bool(re.search("sql", txt)):
            return 1
        else:
            return 0

    def getDf(self):
        return self.df_

    def getFeatures(self):
        return self.X


@app.route('/')

def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    :return:

    Pred_list =[]
    for x in request.form.values():
        Pred_list.append(x)
    '''
    df_predict = pd.DataFrame()
    df_predict['metier'] = [request.form.get('metier')]
    df_predict['Departement'] = [request.form.get('Departement')]
    df_predict['contrat'] = [request.form.get('contrat')]
    df_predict['experience'] = [request.form.get('experience')]
    df_predict['Description'] = [request.form.get('Description')]

    preproc1 = PreprocessJob(df_predict)
    X = preproc1.getFeatures()



    prediction = model.predict(X)



    return render_template('index.html', prediction_text = 'Votre salaire annuel est entre  {} et {}'.format(round(prediction[0]-5478),(round(prediction[0]+5478))))



if __name__=="__main__":
    app.run(debug=True)



