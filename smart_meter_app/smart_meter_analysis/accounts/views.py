from django.shortcuts import redirect, render
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.contrib import messages
import pandas as pd
import plotly.express as px   
import statistics as stats
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import warnings
import itertools
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignUpForm
from .models import User
import datetime
import string
from django.views.decorators.csrf import csrf_exempt

letters = string.ascii_letters + string.punctuation

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('smart_app:signin')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_username = request.POST.get('username')
        meter = str(request.POST.get('meter_number'))
        phone = str(request.POST.get('phone_number'))
        meter_1 = meter
        meter = 't' + meter
        
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if User.objects.filter(phone_number=phone).exists():
            messages.info(request, 'Phone number exists.')
            return redirect('smart_app:signup')
        elif User.objects.filter(meter_number= meter).exists():
            messages.info(request, 'Meters number exists.')
            return redirect('smart_app:signup')
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        else:
            for item in phone:    
                if item in letters:
                    messages.info(request, 'Please enter a valid phone number.')
                    return redirect('smart_app:signup')
            for item in meter_1:
                if item in letters:
                    messages.info(request, 'Please enter a valid meter number.')
                    return redirect('smart_app:signup')
        if form.is_valid():
            form.save()
            user_1 = User.objects.get(username = user_username)
            meter_number = user_1.meter_number
            meter_number = 't' + str(meter_number)
            cursor = connection.cursor()
            date_value = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            cursor.execute("CREATE TABLE %s (balance REAL NOT NULL, date DATE NOT NULL);" % meter_number)
            # cursor.execute("INSERT INTO %s VALUES (0, to_date(%s::text, 'YYYY-MM-DD'));" % (meter_number, date_value))
            cursor.execute("INSERT INTO %s VALUES (0, '%s')" % (meter_number, date_value))
            SignUpForm()
            return redirect('smart_app:signin')
    else:
        form = SignUpForm()
    return render(request, 'smartapp/register.html',{'form': form})

@csrf_exempt
def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        user_username = request.POST.get('username')
        analysis_type = request.POST['analysis']
        pass_word = request.POST.get('password')
        
        #Check if user exists
        if not User.objects.filter(username=user_username).exists():
            messages.info(request, "Username does not exist")
            return redirect('smart_app:signin')
        elif analysis_type == "":
            messages.info(request, "Select a mode of prediction")
            return redirect('smart_app:signin')
        else:
            user_1 = User.objects.get(username = user_username)
            meter_number = user_1.meter_number
            meter_number = 't' + str(meter_number)
            if form.is_valid():
                user = form.get_user()
                display_results(meter_number, analysis_type)
                chart ,pred_type,title = display_results(meter_number, analysis_type)
                login(request, user)
                form = AuthenticationForm()
                return render(request, 'smartapp/results.html', {'chart': chart, 'pred_type': pred_type, 'title': title,'user': user})
    else:
        form = AuthenticationForm()
    return render(request, 'smartapp/signin.html',{'form': form})
    
   
def display_results(meter_number, analysis_type):
    balance = []
    date = []
    cursor = connection.cursor()
    cursor.execute("SELECT date, balance FROM " + meter_number)
    fetch = cursor.fetchall()
    fetch_len = len(fetch)
    for item in fetch:
        date.append(item[0])
        balance.append(item[1])
    if fetch_len > 1:
        if analysis_type == 'week':
            fig = px.line(
                x = date[-7:],
                y = balance[-7:],
                # title = "Graph of user's consumption against time for last week",
                labels= {'x' : 'Date', 'y' : 'Balance'},
                markers=True,
            )
            
            fig.update_layout(title={
                'font_size' : 22,
                'xanchor' : 'center',
                'x' : 0.5,
            })
    
            chart = fig.to_html()
            title = "Graph of user's consumption against time for last week"
            pred_type = prediction_pattern(balance, date)
            return chart, pred_type, title

        elif analysis_type == 'month':
            fig = px.line(
                x = date[-30:],
                y = balance[-30:],
                # title = "Graph of user's consumption against time for last month",
                labels= {'x' : 'Date', 'y' : 'Balance'},
                markers=True,
            )
            
            fig.update_layout(title={
                'font_size' : 22,
                'xanchor' : 'center',
                'x' : 0.5,
            })
            
            chart = fig.to_html()
            title = "Graph of user's consumption against time for last month"
            pred_type = prediction_pattern(balance, date)
            return chart, pred_type, title
        
    else:
        if analysis_type == 'week':
            fig = px.line(
                x = date[:],
                y = balance[:],
                # title = "Graph of user's consumption against time for last week",
                labels= {'x' : 'Date', 'y' : 'Balance'},
                markers=True,
            )
            
            fig.update_layout(title={
                'font_size' : 22,
                'xanchor' : 'center',
                'x' : 0.5,
            })
    
            chart = fig.to_html()
            title = "Graph of user's consumption against time for last week"
            pred_day = 'GH₵0.00'
            pred_week = 'GH₵0.00'
            pred_month = 'GH₵0.00'
            pred_type = [
                {'day' : pred_day, 'week' : pred_week, 'month' :pred_month}
            ]
            return chart, pred_type, title

        elif analysis_type == 'month':
            fig = px.line(
                x = date[:],
                y = balance[:],
                # title = "Graph of user's consumption against time for last month",
                labels= {'x' : 'Date', 'y' : 'Balance'},
                markers=True,
            )
            
            fig.update_layout(title={
                'font_size' : 22,
                'xanchor' : 'center',
                'x' : 0.5,
            })
            
            chart = fig.to_html()
            title = "Graph of user's consumption against time for last month"
            pred_day = 'GH₵0.00'
            pred_week = 'GH₵0.00'
            pred_month = 'GH₵0.00'
            pred_type = [
                {'day' : pred_day, 'week' : pred_week, 'month' :pred_month}
            ]
            return chart, pred_type, title
        


def prediction_pattern(balance, Date):
    smart_meter_data = pd.DataFrame(list(zip(Date, balance)), columns=['date', 'balance'])
    #--------------------------------------------------------------------------------------------------------------
    smart_meter_data['Consumption'] = abs(smart_meter_data['balance'].diff()).dropna()
    smart_meter_data['Consumption'] = smart_meter_data['Consumption'].replace(np.nan, 0)
    #------------------------------------------------------------------------------------------------
    for i in range(len(smart_meter_data['Consumption'])):
        if smart_meter_data['Consumption'][i] >= 6:
    #         smart_meter_data['Consumption'] = smart_meter_data['Consumption'].replace(smart_meter_data['Consumption'][i], 5)
            mean_consumption = stats.mean(smart_meter_data['Consumption'][:i])
            if mean_consumption <= 6:
                smart_meter_data['Consumption'] = smart_meter_data['Consumption'].replace(smart_meter_data['Consumption'][i], mean_consumption)
            else:
                smart_meter_data['Consumption'] = smart_meter_data['Consumption'].replace(smart_meter_data['Consumption'][i], 5)
    #------------------------------------------------------------------------------------------------   -------------------
    smart_meter_data['Consumption'] = smart_meter_data['Consumption'].dropna()
    prediction = smart_meter_data[['Consumption','date']]
    prediction.index = pd.to_datetime(prediction.date)
    #----------------------------------------------------------------------------------------------------------------------------------------
    ADF_result = adfuller(prediction['Consumption'].dropna())
    while ADF_result[1] >= 0.05:
            d = 0

            abs(prediction['Consumption'].diff()).dropna()

            d = d+1

    else:
            d=0
    x = prediction['Consumption'].dropna().values
    train = x[0:]
    predictions = []
    #----------------------------------------------------------------------------------------------------------------
    warnings.filterwarnings('ignore')
    p=d=q = range(0,3)
    pdq = list(itertools.product(p,d,q))
    param_values = []
    error_values = []
    for param in pdq:
        try: 
            model_arima = ARIMA(train, order=param)
            model_arima_fit = model_arima.fit()
            # print(param,model_arima_fit.aic)
            param_values.append(param)
            error_values.append(model_arima_fit.aic)
        except:
            continue
    min_error_value = min(error_values)
    error_value_index = error_values.index(min_error_value)
    param_value = param_values[error_value_index]
    # param_value = (0,0,2)
    #----------------------------------------------------------------------------------------------------------------------
    model_arima = ARIMA(train, order=param_value)
    model_arima_fit = model_arima.fit()
    forecast_values = []
    forecast_values = model_arima_fit.forecast(steps=8)[0]
    # print(forecast_values)
    min_forecast_value = np.min(forecast_values)
    max_forecast_value = np.max(forecast_values)
    #----------------------------------------------------------------------------------------------------------------------
    print('Your average daily consumption is between GH₵%s and GH₵%s'% (round(min_forecast_value,2), round(max_forecast_value,2)))
    print('Your average weekly consumption is GH₵%s and GH₵%s'%(round(7 * min_forecast_value,2),round(7 * max_forecast_value,2)))
    print('Your average monthly consumption is GH₵%s and GH₵%s'%(round(30 * min_forecast_value,2),round(30 * max_forecast_value,2)))
    
    pred_day = 'GH₵%s'% round(min_forecast_value,2)
    pred_week = 'GH₵%s' %round(7 * min_forecast_value,2)
    pred_month = 'GH₵%s'%round(30 * min_forecast_value,2)
    pred_type = [
                {'day' : pred_day, 'week' : pred_week, 'month' :pred_month}
            ]
    return pred_type
    
    
    
        
    
