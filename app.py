import pathlib
import google
from flask import Flask, request, render_template, session
import os
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

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

app.secret_key = "CodeSpecialit.com"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "956614726164-vrjnh0qqumcnulh25mbiab7fsnnk7kpe.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://interest-calci-oaut.herokuapp.com/callback"
)
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/protected_area")
@login_is_required
def protected_area():
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
    principle = p
    rate = r
    start = s_date
    end = e_date
    out1 = [principle, rate, start, end, d_output, s_output, s_output+p, c_output-p, c_output]
    s1 = "1) Principle Amount is: {0}".format(out1[0])
    s2 = "2) Rate of Interest is: {0} x 12 %".format(out1[1])
    s3 = "3) Start Date: {0}".format(out1[2])
    s4 = "4) End Date: {0}".format(out1[3])
    s5 = "5) Total Number of Days is:  {0}".format(out1[4])
    s6 = "6) Interest for the Amount with respect to SI is: {0}".format(out1[5])
    s7 = "7) Final Amount with respect to SI is: {}".format(out1[6])
    s8 = "8) Interest for the Amount with respect to CI is: {}".format(out1[7])
    s9 = "9) Final Amount with respect to CI is: {}".format(out1[8])
    return render_template('index.html', prediction_text1=s1, prediction_text2=s2,prediction_text3=s3, prediction_text4=s4,prediction_text5=s5, prediction_text6=s6,prediction_text7=s7, prediction_text8=s8,prediction_text9=s9)

if __name__ == "__main__":
    app.run(debug=True)
