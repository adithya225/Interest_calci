import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
def total_days(s_date,e_date):
    start_date = list(map(int, s_date.split('/')))
    end_date = list(map(int, e_date.split('/')))
    sd, sm, sy = start_date[0], start_date[1], start_date[2]
    ed, em, ey = end_date[0], end_date[1], end_date[2]
    if ed<sd:
        ed1=ed+30
        em1=em-1
        days=ed1-sd
        if em1<sm:
            em2=em1+12
            ey1=ey-1
            months=em2-sm
            if ey1<sy:
                print("please check your values")
            else:
                years=ey1-sy
        else:
            months=em1-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy
    else:
        days=ed-sd
        if em<sm:
            em3=em+12
            ey2=ey-1
            months=em3-sm
            if ey2<sy:
                print("please check your details")
            else:
                years=ey2-sy
        else:
            months=em-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy


    td=days+(months*30)
    td1=td+(years*360)
    return td1
def c_interest(p,r,s_date,e_date):
    rt=(r*12)/100
    start_date = list(map(int, s_date.split('/')))
    end_date = list(map(int, e_date.split('/')))
    print(start_date,end_date)
    sd, sm, sy = start_date[0], start_date[1], start_date[2]
    ed, em, ey = end_date[0], end_date[1], end_date[2]
    if ed<sd:
        ed1=ed+30
        em1=em-1
        days=ed1-sd
        if em1<sm:
            em2=em1+12
            ey1=ey-1
            months=em2-sm
            if ey1<sy:
                print("please check your values")
            else:
                years=ey1-sy
        else:
            months=em1-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy
    else:
        days=ed-sd
        if em<sm:
            em3=em+12
            ey2=ey-1
            months=em3-sm
            if ey2<sy:
                print("please check your details")
            else:
                years=ey2-sy
        else:
            months=em-sm
            if ey<sy:
                print("please check your values")
            else:
                years=ey-sy


    td=days+(months*30)
    td1=td+(years*360)
    t=td1/360

    i1 = (p*(1+rt)**(int(t))) - p
    p1 = i1 + p
    i2 = (p1*rt*(t-int(t))) + p1
    return i2
def s_interest(principle, r, s_date, e_date):
    rt=(r*12)/100
    start_date = list(map(int, s_date.split('/')))
    end_date = list(map(int, e_date.split('/')))
    sd, sm, sy = start_date[0], start_date[1], start_date[2]
    ed, em, ey = end_date[0], end_date[1], end_date[2]
    if ed < sd:
        ed1 = ed + 30
        em1 = em - 1
        days = ed1 - sd
        if em1 < sm:
            em2 = em1 + 12
            ey1 = ey - 1
            months = em2 - sm
            if ey1 < sy:
                print("please check your values")
            else:
                years = ey1 - sy
        else:
            months = em1 - sm
            if ey < sy:
                print("please check your values")
            else:
                years = ey - sy
    else:
        days = ed - sd
        if em < sm:
            em3 = em + 12
            ey2 = ey - 1
            months = em3 - sm
            if ey2 < sy:
                print("please check your details")
            else:
                years = ey2 - sy
        else:
            months = em - sm
            if ey < sy:
                print("please check your values")
            else:
                years = ey - sy

    td = days + (months * 30)
    td1 = td + (years * 360)
    t = td1 / 360

    interest = principle*t*rt
    return interest

c_model = c_interest
s_model = s_interest



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    features = [str(x) for x in request.form.values()]
    print(features)
    p = int(features[0])
    print(p)
    r = float(features[1])
    print(r)
    s_date = str(features[2])
    e_date = str(features[3])
    c_prediction = c_model(p,r,s_date,e_date)
    s_prediction = s_model(p,r,s_date,e_date)
    days = total_days(s_date,e_date)
    c_output = round(c_prediction, 0)
    s_output = round(s_prediction, 0)
    d_output = days
    out1 = [d_output, s_output, s_output+p, c_output-p, c_output]
    s = '''\
    ... Total Number of Days is {0} .
    ######################################################################################
    ... Interest for the Amount with respect to SI is {1}.
    ... Final Amount with respect to SI is {2}.
    #######################################################################################
    ... Interest for the Amount with respect to CI is {3}.
    ... Final Amount with respect to CI is {4}.
    #######################################################################################\
    ... '''.format(out1[0], out1[1],out1[2],out1[3],out1[4])
    #     out = '''Price with repect to RANDOM FOREST REGRESSION is {0} \n Price with respect to LINEAR REGRESSION is {1}'''.format(out1[0],out1[1])
    return render_template('index.html', prediction_text=s)


if __name__ == "__main__":
    app.run(debug=True)