import urllib
import json
import os
import  pandas as pd

from flask import Flask
from flask import request
from flask import make_response
import pickle

app= Flask(__name__)
model = pickle.load(open("model.pkl","rb"))



@app.route('/webhook', methods=['POST'])
def webhook():
        req = request.get_json(silent=True, force=True)
        res = json.dumps(req['queryResult']['parameters'], indent=4)
        int_features=json.loads(res)
        print(int_features)
        final_features=pd.DataFrame({'age':[int(int_features['age']['amount'])],'num_preg':[int(int_features['num_preg'])],'glucose_conc':[int(int_features['glucose_conc'])],'diastolic_bp':[int(int_features['diastolic_bp'])],'insulin':[int(int_features['insulin'])],'bmi':[float(int_features['bmi'])],'diab_pred':[float(int_features['diab_pred'])],'skin':[float(int_features['skin'])]})
        r=get_data(final_features)
        print(r)
        r=json.dumps(r)
        result = make_response(r)
        result.headers['Content-Type'] = 'application/json'
        return result

def get_data(final_features):
   prediction=model.predict_proba(final_features)
   pred=(prediction[0][0])
   if (pred<0.5):
        output='You have '+ str((1-pred)*100)+'%'+' possibility of having Diabetes.Please take immediate action to cure your self.'
   elif (0.5<=pred<0.75):
        output='You have '+ str((1-pred)*100)+'%'+' possibility of having Diabetes.You have to be careful and take some actions.'
   elif (pred>0.75):
        output='You have '+ str((1-pred)*100)+'%'+' possibility of having Diabetes.You are safe'
 
    
   return {
       "fulfillmentText" : output,
       "Prediction_message": "prediction"
        
   }
 
if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
    
