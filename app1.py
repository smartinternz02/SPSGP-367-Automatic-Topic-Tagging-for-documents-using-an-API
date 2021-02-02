from flask import Flask,render_template,request
import numpy as np
import re
import requests
import json
import csv
import pandas as pd

app = Flask(__name__)

def check(output):
    url = "https://rapidapi.p.rapidapi.com/generate/"
    payload = {"text": output}
    #print(payload)
    headers = {
    'x-rapidapi-key': "537649ff73msh477f6855911bb13p129cf4jsnd5cb001617b2",
    'x-rapidapi-host': "twinword-topic-tagging.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=payload)
    print(response.text)
    return response.json()["topic"]
    #return var


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/summarizer")
def summarizer():
    return render_template('summarizer.html')

@app.route("/summarize",methods=["POST"])
def summarize():
    output = request.form['output']
    output = re.sub(r'[^a-zA-Z.,]'," ",output)
    print(output)

    #essay = check(output) #    API call
    with open('sample.json') as json_file:      #Test using sample json
        essay = json.load(json_file)

    data_file = open('data_file.csv','w')
    csv_writer = csv.writer(data_file)
    count = 0
    for emp in essay:
        print(essay[emp])
        essay[emp] = round(essay[emp],4)
        if count == 0:
            header = ["Type","Probability"]
            csv_writer.writerow(header)
            count += 1
        d = [emp,essay[emp]]
        print(d)
        csv_writer.writerow(d)
    data_file.close()
    df = pd.read_csv('data_file.csv')
    temp = df.to_dict('records')
    print(temp)
    colname = df.columns.values
    return render_template('summary.html',records = temp,colnames = colname)

if __name__=="__main__":
    app.run(debug=True)


