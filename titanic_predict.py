import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

def one_hot(dataframe, name):
    dataframe = pd.concat([dataframe, pd.get_dummies(dataframe[name])
                           .rename(columns=lambda x: name + str(x))], axis=1)
    return dataframe.drop(name, axis=1)



def preprocess_data(data):
    data['Cabin'].fillna('U0', inplace=True)
    data['CabinSection'] = LabelEncoder().fit_transform(data['Cabin'].map(lambda x: x[0]))
    
    data['CabinDistance'] = data['Cabin'].map(lambda x: x[1:])
    data['CabinDistance'] = data['CabinDistance'].map(lambda x: x.split(' ')[0])
    data['CabinDistance'].where(data['CabinDistance'] != '', '0', inplace=True)
    data['CabinDistance'] = data['CabinDistance'].map(lambda x: int(x))
    data['CabinDistance'] = StandardScaler().fit_transform(data['CabinDistance'].values.reshape(-1, 1))

    data['Sex'] = LabelEncoder().fit_transform(data['Sex'])

    data['Embarked'].fillna('S', inplace=True)
    data['Embarked'] = LabelEncoder().fit_transform(data['Embarked'])
    
    data['Name'] = data['Name'].map(lambda x: x.split(',')[1].split('.')[0])
    data['Name'] = LabelEncoder().fit_transform(data['Name'])
    
    data['Fare'].fillna(-1, inplace=True)
    medians = dict()
    for pclass in data['Pclass'].unique():
        median = data.Fare[(data["Fare"] != -1) & (data['Pclass'] == pclass)].median()
        medians[pclass] = median
    for index, row in data.iterrows():
        if row['Fare'] == -1:
            data.loc[index, 'Fare'] = medians[row['Pclass']]
    data['Fare'] = StandardScaler().fit_transform(data['Fare'].values.reshape(-1, 1))
    #data.drop('Fare', axis=1, inplace=True)
    
    data['Age'].fillna(-1, inplace=True)
    medians = dict()
    for title in data['Name'].unique():
        median = data.Age[(data["Age"] != -1) & (data['Name'] == title)].median()
        medians[title] = median
    for index, row in data.iterrows():
        if row['Age'] == -1:
            data.loc[index, 'Age'] = medians[row['Name']]
            
    data['Age'] = StandardScaler().fit_transform(data['Age'].values.reshape(-1, 1))
    
    for index, row in data.iterrows():
        ticket = row['Ticket']
        sibsp = row['SibSp']
        parch = row['Parch']

        if sibsp > 0 or parch > 0:
            ages = list()
            for index2, row2 in data[data['Ticket'] == ticket].iterrows():
                ages.append(row2['Age'])
            data.loc[index, 'Age2'] = min(ages)

        else:
            data.loc[index, 'Age2'] = row['Age']
            
    data['Age2'] = StandardScaler().fit_transform(data['Age2'].values.reshape(-1, 1))
    
    died_titles = ('Don', 'Rev', 'Capt', 'Jonkheer')
    survived_titles = ('Mme', 'Ms', 'Lady', 'Sir', 'Mlle', 'the Countess')
    data['Title_Died'] = data['Name'].apply(lambda x: int(x in died_titles))
    data['Title_Survived'] = data['Name'].apply(lambda x: int(x in survived_titles))

    for title in ('Mr', 'Mrs', 'Miss', 'Master', 'Dr', 'Major', 'Col'):
        data['Title_{}'.format(title)] = data['Name'].apply(lambda x: int(x == title))

    data.drop('Name', axis=1, inplace=True)
    
    data = one_hot(data, 'Pclass')
    #data = one_hot(data, 'Embarked')
    
    data.drop('Cabin', axis=1, inplace=True)
    data.drop('Ticket', axis=1, inplace=True)
    
    return data