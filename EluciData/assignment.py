from flask import Flask, render_template, request,redirect, url_for

import pandas as pd
app = Flask(__name__)



@app.route('/', methods=["POST","GET"])
def upload_file():
    if request.method == 'POST':
        file = request.files["file"]
        print("uploaded file: ",file)
        global df
        df = pd.read_excel(file)
        return redirect(url_for("filter_data"))
        
    else:

        return render_template('mainPage.html')

@app.route('/filter_data')
def filter_data():
    df["Accepted Compound ID"].fillna("No ID", inplace = True) 
    global filtered_data_with_PC
    filtered_data_with_PC = df[df["Accepted Compound ID"].str.endswith(' PC')]
    filtered_data_with_PC.to_excel('filtered_data_with_PC.xlsx')
    global filtered_data_with_LPC
    filtered_data_with_LPC = df[df["Accepted Compound ID"].str.endswith('LPC')]
    filtered_data_with_LPC.to_excel('filtered_data_with_LPC.xlsx')
    global filtered_data_with_plasmalogen
    filtered_data_with_plasmalogen = df[df["Accepted Compound ID"].str.endswith('plasmalogen')]
    filtered_data_with_plasmalogen.to_excel('filtered_data_with_plasmalogen.xlsx')  
    print(filtered_data_with_PC["Accepted Compound ID"])
    
    return redirect(url_for("retention_time_roundoff"))


@app.route('/retention_time_roundoff')
def retention_time_roundoff():
    retention_time = df["Retention time (min)"].copy()
    global retention_time_roundoff
    retention_time_roundoff = retention_time.round(0)
    
    df.insert(3,"retention time roundoff (min)",retention_time_roundoff,True)
    print(df["retention time roundoff (min)"])
    df.to_excel('with_retention_time_roundoff.xlsx')
    return redirect(url_for("mean"))

@app.route('/mean')
def mean():
    
    retention_time_roundoff_values = df.iloc[:,3:].copy()
    print("retention_time_roundoff_values",retention_time_roundoff_values["retention time roundoff (min)"])
    mean_values = retention_time_roundoff_values.groupby("retention time roundoff (min)").mean()
    print('mean_values',mean_values)
    mean_values.to_excel('mean_value.xlsx')
    return render_template('mainPage.html',result = True)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)