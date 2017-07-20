import urllib3, requests, json, os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FloatField, IntegerField
from wtforms.validators import Required, Length, NumberRange
url = 'https://ibm-watson-ml.mybluemix.net'
username = '50d176ad-2480-4e85-8885-cbd54001ed6a'
password = 'a27553b8-352a-4376-a8fa-feb782cd9a5a'
scoring_endpoint = 'https://ibm-watson-ml.mybluemix.net/32768/v2/scoring/3652'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpassw0rd'
bootstrap = Bootstrap(app)
class TentForm(FlaskForm):
Sex = RadioField('Your Gender', coerce=str, choices=[('M','Male'),('F','Female')])
Age = FloatField('Your Age', validators=[NumberRange(1,100)])
Married = RadioField('Your Marital Status', coerce=str, choices=[('Married','Married'), \
('Single','Single'),('Unspecified','Unspecified')])
Job = RadioField('Your Job', coerce=str, choices=[('Executive', 'Executive'), \
('Hospitality' ,'Hospitality'),('Other','Other'),('Professional','Professional'), \
('Retail','Retail'),('Retired','Retired'),('Sales','Sales'),('Student','Student'), \
('Trades','Trades')])
submit = SubmitField('Submit')
@app.route('/', methods=['GET', 'POST'])
def index():
form = TentForm()
if form.validate_on_submit():
Sex = form.Sex.data
form.Sex.data = ''
Age = form.Age.data
form.Age.data = ''
Married = form.Married.data
form.Married.data = ''
Job = form.Job.data
form.Job.data = ''
headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
path = '{}/v2/identity/token'.format(url)
response = requests.get(path, headers=headers)
mltoken = json.loads(response.text).get('token')
scoring_header = {'Content-Type': 'application/json', 'Authorization': mltoken}
payload = {"record":[Sex, Age, Married, Job]}
scoring = requests.put(scoring_endpoint, json=payload, headers=scoring_header)
return render_template('score.html', form=form, scoring=scoring)
return render_template('index.html', form=form)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
app.run(host='0.0.0.0', port=int(port))