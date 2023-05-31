import urllib.request
import json
import os
import ssl
 
def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
 
allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.
 
 
def model_predict(age,sex,bmi,children,smoker,region):
    # Request data goes here
    data = {
        "Inputs": {
            "input1":
            [
                {
                    "age": age,
                    "sex": sex,
                    "bmi": bmi,
                    "children": children,
                    "smoker": smoker,
                    "region": region,
                    "charges":0
                },
            ]
        },
        "GlobalParameters": {
        }
    }
 
    body = str.encode(json.dumps(data))
 
    url = 'http://6b7aee80-5b64-42df-a0cf-ec3faac384b1.eastus2.azurecontainer.io/score'
    api_key = 'e4nCKYVaxfK314dQaWE9NSldB228b2Xf' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
 
    req = urllib.request.Request(url, body, headers)
 
    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_decode = result.decode('utf-8')
        return json.loads(result_decode)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
 
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def formPage():
    return render_template('form.html')
 
@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':
        form_data = request.form
        #Sex
        male = ''
        female = ''
        if form_data['sex']=='male':
            male = 'checked'
        else:
            female = 'checked'
        #Smoker
        smoker_yes = ''
        smoker_no = ''
        if form_data['smoker']=='yes':
            smoker_yes = 'checked'
        else:
            smoker_no = 'checked'
        #Region
        southeast = ''
        southwest = ''
        northwest = ''
        if form_data['region']=='southeast':
            southeast = 'selected'
        elif form_data['region']=='southwest':
            southwest = 'selected'
        else:
            northwest = 'selected'
        result = model_predict(form_data['age'],form_data['sex'],form_data['bmi'],form_data['children'],form_data['smoker'],form_data['region'])
        return render_template('form.html', age = form_data['age'], male = male, female = female, bmi = form_data['bmi'], children = form_data['children'], smoker_yes = smoker_yes, smoker_no = smoker_no, southwest = southwest, southeast = southeast, northwest = northwest,
        prediction = result['Results']['WebServiceOutput0'][0]['Scored Labels'])
 
if __name__ == "__main__":
    app.run()