from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import smtplib
from pyresparser import ResumeParser
from gevent.pywsgi import WSGIServer
import os

# creates SMTP session
    
s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls() 

SUBJECT = "Interview Call"

python_skills = ["ml","ai","matplotlib","seabon",
                 "python","reression","algorithms",
                 "Pandas","data analysis","keras",
                 "tensorflow","artificial intelligence",
                 "data visualization","opencv"]

java_skills  = []


app = Flask(__name__)

@app.route('/')
def homepage():
   return render_template('index.html')
@app.route('/apply_job')
def applyjob():
    return render_template("apply_job.html")


@app.route('/fill_form')
def fillform():
    return render_template("form.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        data = ResumeParser(f.filename).get_extracted_data()
        name = data['name']
        email = data['email']
        skills = data["skills"]
        actual_skills = [i.lower() for i in skills ]
        # using list comprehension
        # checking if string contains list element
        Skills_matched = [ele for ele in actual_skills if(ele in python_skills)]
        if(len(Skills_matched) >= 4 ):
            print("he is eligible")
            #s.login("SI2021IBM04128@smartinternz.com", "SIIBM2021To12")
            s.login("rneelima29@gmail.com", "9290486224") 
            TEXT = "Hello "+name + ",\n\n"+ """Thanks for applying to the
            job post AI/ML Developer , Your skils matches our requirement.
            Kindly let us know the available time for initial round of interview. 
            \n\n\n\n Thanks and Regards, \n\n Talent acquistition Team, \n\n Smartbridge""" 
            message  = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            s.sendmail("rneelima29@gmail.com", email, message)
            s.quit()
            return render_template('form.html',prediction = 
                                   """Thanks  for applying youwill be mailed about
                                   your candidature""")

        else:
            print("sorry we cant process your candidature")
            #s.login("SI2021IBM04128@smartinternz.com", "SIIBM2021To12")
            #s.login("prads.pradeepthi@gmail.com", "oms@1Ram")
            s.login("rneelima29@gmail.com", "9290486224")
            TEXT = "Hello "+name + ",\n\n"+ """Thanks for applying to the job post AI/ML 
            Developer , Your candidature is rejected. 
            \n\n\n\n Thanks and Regards, \n\n Talent acquistition Team, \n\n Smartbridge""" 
            message  = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            s.sendmail("rneelima29@gmail.com", email, message)
            s.quit()
            return render_template('form.html',prediction = 
                                   """Thanks  for applying youwill be 
                                   mailed about your candidature""")
    else:
        return render_template('index.html')
port = os.getenv('VCAP_APP_PORT','8080')
		
if __name__ == '__main__':
   #app.run(debug = True)
   app.secret_key = os.urandom(12)
   app.run(debug=True, host='0.0.0.0', port=port)
   
   
   
   
   
   
   
   
   
