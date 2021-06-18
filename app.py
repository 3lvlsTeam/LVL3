#-- import section ----------------------------------------------------------------------------------------------------------
from functools import reduce
import re , bcrypt,os
from flask import Flask , redirect, url_for, render_template,request,flash
from flask.globals import session
from datetime import datetime, timedelta , date
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import urllib.request
from codes import functions
#------------------------------------------------------------------------------------------------------------------------------



#-- app configratins -----------------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key="3Eg!hS_24vwvEWF34@!r"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database/users.sqlite3'
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False
app.permanent_session_lifetime = timedelta(days=1)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

#-------------------------------------------------------------------------------------------------------------------------------




#-- db configratins ------------------------------------------------------------------------------------------------------------
db = SQLAlchemy(app)
class users(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    username = db.Column(db.String(100),nullable=False)
    user_email = db.Column(db.String(100),nullable=False)
    user_bday = db.Column(db.DateTime,nullable=False)
    user_password = db.Column(db.String(100),nullable=False)
    img_password = db.Column(db.String(100),nullable=True)
    signup_time = db.Column(db.DateTime)

    def __init__(self,first_name,last_name,username,user_email,user_bday,user_password,signup_time,img_password):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.user_email=user_email
        self.user_bday=user_bday
        self.user_password=user_password
        self.signup_time=signup_time
        self.img_password=img_password
    
#-------------------------------------------------------------------------------------------------------------------------------


#------  some functions  -------------------------------------------------------------------------------------------------------

def make_tmp_usr():
    try:
        global usr
        usr = users.query.filter_by(username=session["username"]).first()
    except:pass
def user_is_loged():

    try:
        make_tmp_usr()
        if bcrypt.checkpw(session["password"],usr.user_password):
            if bcrypt.checkpw(session["img_password"],usr.img_password):
                return True
    except:
            return False

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
#-------------------------------------------------------------------------------------------------------------------------------

       



#-- main function -------------------------------------------------------------------------------------------------------------
@app.route("/")
def main():
    return redirect(url_for("home"))
#------------------------------------------------------------------------------------------------------------------------------
    


#-- signup function -----------------------------------------------------------------------------------------------------------
@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        allgood= True
        session["firstname"]= request.form["input_firstname"]
        session["lastname"]= request.form["input_lastname"]
        session["username"]= request.form["input_username"]
        session["useremail"]= request.form["input_email"]
        session["birthdate"]= datetime.strptime(request.form["input_birthdate"],'%Y-%m-%d')
        session["password"]= request.form["input_password1"]
        session["password2"]= request.form["input_password2"]
        today=functions.age.to_integer(date.today())
        birthdate=functions.age.to_integer(session["birthdate"])
        age=today-birthdate
        tempuser= users.query.filter_by(username=session["username"]).first()
        if tempuser:
            flash("username alrady existe, try another one.")
            allgood= False
        email= users.query.filter_by(user_email=session["useremail"]).first()
        if email:
            flash("This Email is alrady used, try another one.")
            allgood= False
        if re.search(r'\d', session["firstname"]):
            flash(" first name must be letters only")
            allgood=False
        if re.search(r'\d', session["lastname"]):
            flash(" last name must be letters only")
            allgood=False
        if re.search(r'[^a-zA-Z0-9]', session["username"]):
            flash("username  must be letters and numbers only")
            allgood=False
        if  functions.pinger.test_if_real(session["useremail"]):
            flash("email is not valid")
            allgood=False
        if age < 180000:
            flash("must be above 18")
            allgood=False
        if session["password"] != session["password2"]:
            flash("password doesn't match")
            allgood=False
        if functions.how_strong.how_strong(session["password"]) < 500:
            flash("password are too weak ")
            allgood=False
        if not allgood:
            return redirect(url_for("signup"))
        if allgood:
            session["password"]=session["password"].encode("utf-8")
            session["password_crybted"]=bcrypt.hashpw(session["password"],bcrypt.gensalt())
            newuser=users(session["firstname"],session["lastname"],session["username"],session["useremail"],session["birthdate"],session["password_crybted"],datetime.now(),None)
            db.session.add(newuser)
            db.session.commit()
            return redirect(url_for("signupF2"))
        

    return render_template("signup.html")


#--------------------------------------------------------------------------------------------------------------------------------



#--- pwget function ------------------------------------------------------------------------------------------------------------
@app.route("/pwgen",methods=["POST","GET"] )
def pwgen():
    
    if request.method == "POST":
        input_gen_numbers = request.form["input_gen_numbers"]
        input_gen_text = request.form["input_gen_text"]
        if functions.pw_maker.conventer_to_list(input_gen_text) < 8:
            flash("enter al lest 8 words")
            return redirect(url_for('pwgen'))
        elif functions.pw_maker.conventer_to_list(input_gen_text) > 7:
            gen_password = functions.pw_maker.password_maker(input_gen_numbers,input_gen_text)
            return render_template("pwgen.html",gen_password=gen_password) 

    return render_template("pwgen.html")
#-------------------------------------------------------------------------------------------------------------------------------


#---- signup 2 function ----------------------------------------------------------------------------------------------------------
@app.route("/signupF2",methods=["POST","GET"])
def signupF2():   
    make_tmp_usr()
    if request.method == "POST":
        session["img_password"]=request.form["img_password"]
        if session['img_password'].count(".")>4:
            session["img_password"]=session["img_password"].encode("utf-8")
            usr.img_password=bcrypt.hashpw(session["img_password"],bcrypt.gensalt())
            db.session.commit()
            flash('Done!')
            return redirect(url_for("signupF3"))
        else:flash("Choose 5 images at least!!")
    directory=functions.directory.directory_maker(usr.id)
    img_list= functions.directory.directory_scaner(directory)
    return render_template("signupF2.html", imgs_list =img_list,directory=directory ,usr=usr)
#------------------------------------------------------------------------------------------------------------------------------



#---- signup 3 function ----------------------------------------------------------------------------------------------------------
@app.route("/signupF3",methods=["POST","GET"])
def signupF3():   
    return render_template("signupF3.html")
#------------------------------------------------------------------------------------------------------------------------------


#---- uploader function --------------------------------------------------------------------------------------------------------
@app.route('/uploader', methods=["POST","GET"])
def uploader():
    make_tmp_usr()
    if not bcrypt.checkpw(session["password"],usr.user_password):
        return redirect(url_for("login"))
    directory="static/images/"+str(usr.id)
    img_list=os.listdir(directory)
    if len(img_list)<5:
        flash("must be at least 5 photos ")
    if request.method=="POST":
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        print(files)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(directory, filename))
            else:
                flash('Allowed image types are - png, jpg, jpeg, gif')      
        return redirect(url_for('uploader'))
        
    return render_template("uploader.html",usr=usr,imgs_list=img_list,directory=directory)   
#-------------------------------------------------------------------------------------------------------------------------------


#--- login function -----------------------------------------------------------------------------------------------------------
@app.route("/login",methods=["POST","GET"])
def login():
    if user_is_loged():
        return redirect(url_for("home") )
    
    if request.method=="POST":
        session.clear()
        session["username"]=request.form["username"]
        session["password"]=request.form["password"].encode("utf-8")
        make_tmp_usr()
        if usr:
            if bcrypt.checkpw(session["password"],usr.user_password):
                return redirect(url_for("loginF2") )
            else:
                flash("login faild.")
        else:
            flash("login faild.")
            
        flash("wrong username or password.")
    return render_template("login.html")
    
#------------------------------------------------------------------------------------------------------------------------------


#--- loginF2 function ----------------------------------------------------------------------------------------------------------
@app.route('/loginF2', methods=['GET', 'POST'])
def loginF2():
    if user_is_loged():
            return redirect(url_for("home") )
    try:        
        if not bcrypt.checkpw(session["password"],usr.user_password):
            flash("ur not loged in yet!")
            return redirect(url_for("login") )
    except:
        flash("ur not loged in yet!")
        return redirect(url_for("login") )

    if usr.img_password == None:
        flash("Pleas Fnish Signing Up First!")
        return redirect(url_for("signupF2"))
   
    if request.method=="POST":
        session["img_password"]=request.form["img_password"].encode("utf-8")
        if bcrypt.checkpw(session["img_password"],usr.img_password):
            return redirect(url_for("home") )
        else:
            flash("wrong order,pleas try again!")
    
    directory=functions.directory.directory_maker(usr.id)
    img_list= functions.directory.directory_scaner(directory)
    return render_template("loginF2.html", imgs_list =img_list, directory=directory ,usr=usr)
#-------------------------------------------------------------------------------------------------------------------------------
  



#-- home function ------------------------------------------------------------------------------------------------------------
@app.route("/home")
def home():
    if user_is_loged():
        return render_template("home.html", usr=usr)
    else:
        flash("You r not loged in!")
        return redirect(url_for("login"))
#------------------------------------------------------------------------------------------------------------------------------


#--- profile function ---------------------------------------------------------------------------------------------------------
@app.route("/profile")
def profile():
    if user_is_loged():
        return render_template("profile.html",usr=usr)
    else:
        flash("You r not loged in!")
        return redirect(url_for("login"))
    
#------------------------------------------------------------------------------------------------------------------------------


#--- logout function -----------------------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    flash("you just loged out")
    return redirect(url_for("main"))
#------------------------------------------------------------------------------------------------------------------------------


#--- code runner function -------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)