from flask import Flask,render_template,request
import numpy as np
import re
import requests
import json
import csv
import pandas as pd

app = Flask(__name__)

def check(output):
    url = "https://twinword-topic-tagging.p.rapidapi.com/generate/"

    querystring = {"text": output}

    headers = {
        'x-rapidapi-key': "d1e49c12c3msh99286f8e9159525p10515bjsnf0ce1a63fea9",
        'x-rapidapi-host': "twinword-topic-tagging.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    return response.json()["topic"]


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/summarizer")
def summarizer():
    return render_template('summarizer.html')

@app.route("/summarize",methods=["POST"])
def summarize():
    #output = request.form['output']
    output = "friend body human work"
    output = re.sub(r'[^a-zA-Z.,]'," ",output)
    print(output)

    #essay = check(output)
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


""" API code
import requests

url = "https://twinword-topic-tagging.p.rapidapi.com/generate/"

querystring = {"text":"Computer science is the scientific and practical approach to computation and its applications. It is the systematic study of the feasibility, structure, expression, and mechanization of the methodical procedures (or algorithms) that underlie the acquisition, representation, processing, storage, communication of, and access to information, whether such information is encoded as bits in a computer memory or transcribed in genes and protein structures in a biological cell. An alternate, more succinct definition of computer science is the study of automating algorithmic processes that scale. A computer scientist specializes in the theory of computation and the design of computational systems."}

headers = {
    'x-rapidapi-key': "d1e49c12c3msh99286f8e9159525p10515bjsnf0ce1a63fea9",
    'x-rapidapi-host': "twinword-topic-tagging.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)"""