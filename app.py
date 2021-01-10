import numpy as np
import pandas as pd
import sklearn
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
app.debug = True
TEMPLATES_AUTO_RELOAD = True

@app.route('/')
def home():
    circuits = pd.read_csv('circuits.csv')  
    # circuitTocircuitId = pd.Series(circuits.circuitId.values,index=circuits.name).to_dict()
    circuitsNames = circuits.name

    drivers = pd.read_csv('drivers.csv')
    driversRefs = drivers.driverRef

    laps = np.arange(87)+1

    position = np.arange(24)+1

    stops = np.arange(10)

    laststops = np.arange(80)

    return render_template('index.html', circuits=circuitsNames,drivers=driversRefs,laps=laps,position=position,stops=stops,laststops=laststops)

@app.route('/predict',methods=['POST'])
def predict():
    
    int_features = [x for x in request.form.values()]

    circuits = pd.read_csv('circuits.csv')
    drivers = pd.read_csv('drivers.csv')
    circuitsNames = circuits.name
    driversRefs = drivers.driverRef
    laps = np.arange(87)+1
    position = np.arange(24)+1
    stops = np.arange(10)
    laststops = np.arange(80)
    
    circuitTocircuitId = pd.Series(circuits.circuitId.values,index=circuits.name).to_dict()
    driverToDriverId = pd.Series(drivers.driverId.values,index=drivers.driverRef).to_dict()
    
    int_features[0] = circuitTocircuitId[int_features[0]]
    int_features[1] = driverToDriverId[int_features[1]]
    
    int_features2 = [int(numeric_string) for numeric_string in int_features]
    
    final_features = [np.array(int_features2)]

    for x in final_features:
        print (x)
        
    prediction = model.predict_proba(final_features)
    print(prediction)
    output = prediction[0][1]
    
    return render_template('index.html', prediction_text='Stop probability is {}'.format(output),circuits=circuitsNames,drivers=driversRefs,laps=laps,position=position,stops=stops,laststops=laststops)

@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    print(data)
    print("OazzazazaEIHFEOIFHEOIFHEOIFH")
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
