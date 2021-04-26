from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)



df = pd.read_csv('./static/BankChurners.csv')
df.to_html(header="true", table_id="table")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/visualize', methods=['POST', 'GET'])
def visual():
    return render_template('plot.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    return render_template('predict.html')

@app.route('/dataset', methods=['POST', 'GET'])
def dataset():
    return render_template('dataset.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        user = request.form

        df_to_predict = pd.DataFrame({
            'Customer_Age': [user['age']],
            'Gender': [user['gender']],
            'Dependent_count': [user['dependent_count']],
            'Education_Level': [user['education']],
            'Marital_Status': [user['marital']],
            'Income_Category': [user['income']],
            'Card_Category': [user['card']],
            'Months_on_book': [user['mob']],
            'Total_Relationship_Count': [user['relation']],
            'Months_Inactive_12_mon': [user['months_inactive']],
            'Contacts_Count_12_mon': [user['contac']],
            'Credit_Limit': [user['card limit']],
            'Total_Revolving_Bal': [user['revolve_bal']],
            'Avg_Open_To_Buy': [user['avg_o']],
            'Total_Amt_Chng_Q4_Q1': [user['amt_q4']],
            'Total_Trans_Amt': [user['trans_amt']],
            'Total_Trans_Ct': [user['trans_ct']],
            'Total_Ct_Chng_Q4_Q1': [user['ct_chg']],
            'Avg_Utilization_Ratio': [user['avg_util']]
        
        })

        churn = model.predict(df_to_predict)

        if churn == 0:
            attr = 'Retain'
        else:
            attr = 'Churn'

        return render_template('result.html', data=user, pred=attr)


if __name__ == '__main__':

    filename = 'rff_tuned.sav'
    model = pickle.load(open(filename, 'rb'))

    app.run(debug=True, port=5000)