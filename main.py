from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_login import logout_user
import requests
import boto3
import simplejson as json
import jsonify
import pandas as pd
import random
import time
from datetime import datetime

#Wallet balance API: https://ss979hyehb.execute-api.ap-south-1.amazonaws.com/WalletBalance
app = Flask(__name__)
random.seed()  # Initialize the random number generator
#api to add money to wallet: https://l1gdzvb6k6.execute-api.ap-south-1.amazonaws.com/addwallamount

@app.route('/')
@app.route('/home')
def home():
    title = "Personal Expense Tracker"
    
    return render_template("index2.html", title = title)


@app.route('/chart2')
def chart2(chartID = 'chart_ID', chart_type = 'line', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    title = {"text" : 'Monthly Expenses'}
    user='nbalu@gmail.com'
    expense_date_from = ''
    expense_date_to = ''
    params = "user="+user+"&expense_date_from="+expense_date_from+"&expense_date_to="+expense_date_to
    print(params)
    series_new=fetchExpenses(params)
    #print(type(series_new))
    exp_dates = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                exp_dates.append(item['expense_date'])
    #print("("+'\"categories\"' +": "+ str(exp_dates)+")")    
    home_expenses = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                home_expenses.append(item['home_expenses'])
    seriesopen = "["
    prefixstr = "{" + '\"name\"' + ": "
    datastr = ", " + '\"data\"' + ": "
    suffixstr = "},"
    suffixstr2 = "}"
    seriesend = "]"
    homeexp = seriesopen + prefixstr + '\"Home Expenses\"' +  datastr + str(home_expenses) + suffixstr
    medical_expenses = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                home_expenses.append(item['medical_expenses'])
    medicalexp = prefixstr + '\"Medical Expenses\"' +  datastr + str(medical_expenses) + suffixstr
    vehicle_expenses = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                home_expenses.append(item['vehicle_expenses'])
    vehicleexp = prefixstr + '\"Vehicle Expenses\"' +  datastr + str(vehicle_expenses) + suffixstr2 + seriesend
    series = (homeexp + medicalexp + vehicleexp)
    print(series)
    #xAxis = {"categories": ['05/25/2021', '05/26/2021', '05/27/2021']}
    xAxis = "("+'\"categories\"' +": "+ str(exp_dates)+")"
    print(xAxis)
    yAxis = {"title": {"text": 'Expense'}}    
    return render_template('index1.html', chartID=chartID, chart=chart, title=title, series=series,  xAxis=xAxis, yAxis=yAxis)

@app.route('/chart')
def chart():
    def generate_random_data():
        while True:
            json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generate_random_data(), mimetype='text/event-stream')

def setExpenses(params): 
    print(params)
    url = "https://ket0h58q15.execute-api.ap-south-1.amazonaws.com/ExpenseAPI?"+params
    status = requests.request("GET",url)
    print(status.json())
    return status.json()
    
def fetchExpenses(params):
    url="https://5996kr662d.execute-api.ap-south-1.amazonaws.com/ExpenseQA?"+params
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

def walletBalance(params):
    url="https://ss979hyehb.execute-api.ap-south-1.amazonaws.com/WalletBalance?"+params
    status = requests.request("GET",url)
    print(status.json())
    return status.json()


# Function to check user credentials - AWS API User
def check(user):
    url="https://nirmgp3j2c.execute-api.ap-south-1.amazonaws.com/fetchuser?user="+user  
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

# Function to add amount to wallet - AWS API Add Money
def updatewallet(params):
    url="https://l1gdzvb6k6.execute-api.ap-south-1.amazonaws.com/addwallamount?"+params 
    status = requests.request("GET",url)
    print(status.json())
    return status.json()

@app.route('/wallet')
def wallet():
    return render_template('addmoney.html')

# Function to fetch current wallet balance - AWS API Wallet Balance
@app.route('/dashboard')
def dashboard():
    user = "nbalu@gmail.com"
    params="user="+user
    data=walletBalance(params)
    print(type(data))
    if('errorType' in data):
            return render_template('Login1.html', pred="Wallet could not be updated. Your wallet balance has not changed.")
    else:
            return render_template('dashboard.html', pred=data)

# Function to add amount to wallet - AWS API Add money to wallet
@app.route('/addmoneypage', methods=['GET','POST'])
def addmoneypage() :
    user=request.form['user']
    amount = request.form['amount']
    #Add validation to user and amount fields before submit
    params = "user="+user+"&amount="+amount
    print(params)

    data = updatewallet(params)
    print(type(data))
    
    if('errorType' in data):
        return render_template('addmoney.html', pred="Wallet could not be updated. Your wallet balance has not changed.")
    else:
        return render_template('addmoney.html', pred="Wallet has been updated successfully and your "+data)
    

@app.route('/about')
def aboutpage():

    title = "About this site - PET"
    paragraph = ["Will this chart work with dynamic values set?"]

    pageType = 'about'

    return render_template("index.html", title=title, paragraph=paragraph, pageType=pageType)

@app.route('/nmlgraph', methods=['GET','POST'])
def nmlgraph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
    user='nbalu@gmail.com'
    expense_date_from = ''
    expense_date_to = ''
    params = "user="+user+"&expense_date_from="+expense_date_from+"&expense_date_to="+expense_date_to
    print(params)
    series_new=fetchExpenses(params)

    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, pageType=pageType)

@app.route('/graph', methods=['GET','POST'])
def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 500):
    user='nbalu@gmail.com'
    expense_date_from = ''
    expense_date_to = ''
    params = "user="+user+"&expense_date_from="+expense_date_from+"&expense_date_to="+expense_date_to
    print(params)
    series_new=fetchExpenses(params)
    #print(type(series_new))
    exp_dates = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                exp_dates.append(item['expense_date'])
    print("("+'\"categories\"' +": "+ str(exp_dates)+")")
    xAxis_ds = "("+'\"categories\"' +": "+ str(exp_dates)+")"
    print(xAxis_ds)
    home_expenses = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                home_expenses.append(item['home_expenses'])
    seriesopen = "["
    prefixstr = "{" + '\"name\"' + ": "
    datastr = ", " + '\"data\"' + ": "
    suffixstr = "},"
    suffixstr2 = "}"
    seriesend = "]"
    homeexp = seriesopen + prefixstr + 'Home Expenses' +  datastr + str(home_expenses) + suffixstr
    medical_expenses = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                home_expenses.append(item['medical_expenses'])
    medicalexp = prefixstr + '\"Medical Expenses\"' +  datastr + str(medical_expenses) + suffixstr
    vehicle_expenses = []
    for k, v in series_new.items():
        if k == 'Items':
            for item in series_new['Items']:
                home_expenses.append(item['vehicle_expenses'])
    vehicleexp = prefixstr + '\"Vehicle Expenses\"' +  datastr + str(vehicle_expenses) + suffixstr2 + seriesend
    series_ds = (home_expenses , medical_expenses , vehicle_expenses)
    print(series_ds)
    subtitleText = 'Expense Summary'
    pageType = 'graph'
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType" : 'x'}    
    title = {"text" : 'Monthly Expenses'}
    series = {"name" : 'Monthly Expenses', "data":series_ds}
    xAxis = {"type": "datetime"}
    yAxis = {"title": {"text": 'Expenses'}}
    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, pageType=pageType)

	
@app.route('/login')
def login():
    return render_template('Login1.html')

@app.route('/loginpage', methods=['POST'])
def loginpage():
    user = request.form['user']
    passw = request.form['passw']
    print(user,passw)
    data = check(user)
    if('errorType' in data):
        return render_template('Login1.html', pred="The username is not found, recheck the spelling or please register.")
    else:
        if(passw==data['passw']):
            return redirect(url_for('dashboard'))
        else:
            return render_template('Login1.html', pred="Login unsuccessful. You have entered the wrong password.")
    
@app.route('/expense')
def expense():
    return render_template('expense.html')

@app.route('/expensepage', methods=['POST'])
def expensepage() :
    user=request.form['user']
    expensedate = request.form['expensedate']
    category = request.form['expensetype']
    expenseamount = request.form['expenseamount']

    # Check which type of expense is being updated
    if(category=='medical_expenses'):
        #medical_expenses = request.form['expenseamount']
        params = "user="+user+"&expense_date="+expensedate+"&medical_expenses="+expenseamount+"&home_expenses="+"0"+"&vehicle_expenses="+"0"
    elif(category=='home_expenses'):
        #home_expenses = request.form['expenseamount']
        params = "user="+user+"&expense_date="+expensedate+"&medical_expenses="+"0"+"&home_expenses="+expenseamount+"&vehicle_expenses="+"0"
    elif(category=='vehicle_expenses'):
        #vehicle_expenses = request.form['expenseamount']
        params = "user="+user+"&expense_date="+expensedate+"&medical_expenses="+"0"+"&home_expenses="+"0"+"&vehicle_expenses="+expenseamount
    else:
        render_template('expense.html', pred="Expense type is unauthorized in system.")

    response = setExpenses(params)

    json_object = json.dumps(response)
    print(json_object)
    	
    if('errorType' in json_object):
    	return render_template('expense.html', pred="Expense could not be added. Your wallet balance has not changed.")
    else:
    	return render_template('expense.html', pred=json_object)
    	     
	
@app.route('/registration')
def registration():
    return render_template('register.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
	    name = request.form.get('name')
	    user = request.form.get('user')
	    phone = request.form.get('phone')
	    city = request.form.get('city')
	    occupation = request.form.get('occupation')
	    passw = request.form.get('passw')
	    #passparam = hash_password(passw)
	    #x = [x for x in request.form.values()]
	    #params = "name="+x[0]+"&user="+x[1]+"&phone="+x[2]+"&city="+x[3]+"&occupation="+x[4]+"&passw="+x[5]
	    params="name="+name+"&user="+user+"&phone="+phone+"&city="+city+"&occupation="+occupation+"&passw="+passw
	    if('errorType' in check(user)):
	    	url = "https://nqwsosw3ag.execute-api.ap-south-1.amazonaws.com/QA?"+params
	    	response = requests.get(url)
	    	return render_template('register.html', pred="Registration Successful, please login using your details")
	    else:
	    	return render_template('register.html', pred="You are already a member, please login using your details")
        
@app.route("/logout")
def logout():   
   logout_user()        # Delete Flask-Login's session cookie       
   return redirect(url_for('login'))        

if __name__ == "__main__":
	app.run(port=8500,debug=True,passthrough_errors=True)