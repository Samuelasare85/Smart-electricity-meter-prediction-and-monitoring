import requests
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pmd
import itertools
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime

#url = "https://enersmart.sperixlabs.org/balance"
#payload ="meter=14124356"
#headers = {
#  'Accept': '*/*',
#  'Origin': 'https://enersmart.sperixlabs.org',
#  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
#
#}
#
#response = requests.request("POST", url, headers=headers, data=payload)
#result = response.json()
#print (result)
#source of file to be determined

#def get_energy_data(file_name:str):
    
df=pd.read_excel('Data Log.xlsx',parse_dates=[11])
df['Consumption'] = abs(df['Balance'].diff().dropna())
for i in df['Consumption']:
        #mean_at_i = df[ 'Consumption' ].iloc[ [0,pd.Index(i)] ].mean(axis=0)
        new_num = np.random.randint(29, 31)
        if i >=5:
            df["Consumption"].replace({i:new_num}, inplace=True)
df[['date','Consumption']]
#new_table.index = pd.to_datetime(new_table.date)

#TEST STATIONARITY
ADF_result  = adfuller(df['Consumption'].dropna())[1]
d = 0
while ADF_result > 0.05:
    
    abs(df['Consumption'].diff()).dropna()
    
    d = d+1
    
else:
    d=0
comValues = df['Consumption'].values
#train = comValues[0:int(0.75*len(comValues))]#majority of data
#test = comValues[int(0.75*len(comValues)): ] #use all for train rather||remaining data
train = comValues[0:]#majority of data
predictions = []


#ARIMA MODEL
p=d=q = range(0,8)
pdq = list(itertools.product(p,d,q))
for param in pdq:
    try:
        
        model_arima = ARIMA(train,param)
        model_arima_fit = model_arima.fit()
        aicValue = np.array(model_arima_fit.aic, param)
        leastAicValue_point = aicValue[np.argmin(aicValue[:,0])][1]
        p_new = leastAicValue_point[0]
        d_new = leastAicValue_point[1]
        q_new = leastAicValue_point[2]
        
    except:
        continue
model_arima=ARIMA(train,order=(p_new,d_new,q_new)) 
model_arima_fit=model_arima.fit()
#def makePrediction(duration): 
#  times_to_predict = ['A week from Now', 'A month from Now']  
predictions=model_arima_fit.forecast(steps=7)[0]
print (predictions)

    