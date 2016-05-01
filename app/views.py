
"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session, flash
from app import db

from flask.ext.wtf import Form 
from wtforms import * # other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import myprofile
from app.forms import LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app import oid, lm



import requests
from bs4 import BeautifulSoup
import urlparse
import sys
import json
import smtplib
import string
import hashlib

class ProfileForm(Form):
     name = TextField('First Name', validators=[Required()])
     email = TextField('Email', validators=[Required()])
     password = TextField('Password', validators=[Required()])
     




    
###
# Routing for your application.
###
@lm.user_loader
def user_loader(id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return myprofile.query.get(id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/api/user/login', methods=['POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    
    error = None
    if request.method == 'POST':
        user_email = request.form['email']
        user_pass = request.form['password']
        
        
        profile = myprofile.query.filter(myprofile.email == user_email).first()
        
        
        if profile.email != user_email or profile.password != user_pass:
            error = 'Invalid Credentials. Please try again.'
        else:
            userString = user_email + " " + user_pass
            hash_object = hashlib.md5(userString)
            nowUser = profile.email
            session['nowUser'] = nowUser
            response = app.make_response(redirect(url_for('home', nowUser=nowUser)))
            response.headers['Authorization'] = 'Basic' + " " + (hash_object.hexdigest())
            return response
    return render_template('login.html', form=form)
    
@app.route("/logout")

def logout():
    logout_user()
    return render_template('logout.html')
    
@app.route('/mail')
def mail():
    """Render the website's mail page."""
    return render_template('share_page.html')
    
@app.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    test = request.form['choices']
    test1 = test[1:-1]
    testnew = test1.replace('"','')
    
    test3 = testnew.split(",")
    #test2 = test3[1]
    
    for i in test3:
        import smtplib
        import string
        
        fromname = 'dacx77@gmail.com'
        fromaddr = 'dacx77@gmail.com'
        toname = 'Share to a friend'
        toaddr = i
        subject = 'Sharing my wishlist'
        msg = 'Message'
        
        # Create the message
        BODY = string.join((
            "From: %s" % fromaddr,
            "To: %s" % toaddr,
            "Subject: %s" % subject ,
            "",
            msg
            ), "\r\n")
            
        # Credentials (if needed)
    
        username = 'dacx77@gmail.com'
    
        password = 'pldvmqjwmedemezr'
    
        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, [toaddr], BODY)
        server.quit()
            
    return render_template('mailSuccess.html', emails=test3)
                           
@app.route('/api/thumbnail/process', methods=['POST','GET'])
def home():
    """Render website's home page."""
    nowUser = request.args['nowUser']  
    nowUser = session['nowUser']
    
    
    
    
    profile = myprofile.query.filter(myprofile.email == nowUser).first()
    return render_template('home.html', nowUser = nowUser, profile=profile)

@app.route('/api/user/:id/wishlist', methods=['POST','GET'])
def showSubmit():
    if request.method == "POST":
        picList=[]
        website = request.form['website']
        
        url = website
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        picList = [];
        image = "<img src='%s'>"
        for img in soup.findAll("img", src=True):
            if "sprite" not in img["src"]:
                message = image % urlparse.urljoin(url, img["src"])
                
                
                picList.append(message)
    
        
    
    return render_template('thumb_action.html', website=website, picList=picList)

'''@app.route('/urladd', methods=['POST','GET'])    
def urlAdd():
    if request.method == "POST":
          
        currentUser = session['nowUser']
        url_chosen = request.form['chosenThumb']
        profile = myprofile.query.filter(myprofile.email == nowUser).first()
        
        profile.url = url_chosen
        #db.session.commit()
        
        
    return render_template('url_added.html', url_chosen=url_chosen)'''


    
@app.route('/urladd', methods=['POST','GET'])    
def urlAdd():
    if request.method == "POST":
          
        nowUser = session['nowUser']
        url_chosen = request.form['chosenThumb']
        profile = myprofile.query.filter(myprofile.email == nowUser).update({'url': str(url_chosen)})
       
        db.session.commit()
        
    return render_template('url_added.html', url_chosen=url_chosen)
    
    

@app.route('/api/user/register', methods=['POST','GET'])
def profile_add():
    import os
    from flask import Flask, request, redirect, url_for
    from werkzeug import secure_filename
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        
        
        # write the information to the database
        newprofile = myprofile(name=name,email=email,password=password, url = "")
        db.session.add(newprofile)
        db.session.commit()

        return "Name: {}, Email: {} was created".format(request.form['name'],request.form['email'])

    form = ProfileForm()
    return render_template('profile_add.html',form=form)

@app.route('/profiles',methods=["POST","GET"])
#@login_required
def profile_list():
    import json
    profiles = myprofile.query.all()
    if request.method == "GET":
        profList = str(profiles)
        
        return jsonify({"users":profList})
            #return jsonify({"id":[i].id, "sex":[i].sex, "image":[i].image, "high_score":[i].high_score, "tdollars":[i].tdollars})
    return render_template('profile_list.html',profiles=profiles)

@app.route('/profile/<int:id>',methods=["POST","GET"])
def profile_view(id):
    profile = myprofile.query.get(id)
    if request.method == "GET":
        return jsonify({"data":"no instructions for GET"})
    if request.method == "POST":
        
        return jsonify({"id":profile.id, "email":profile.email, "url":profile.url})
    return render_template('profile_view.html',profile=profile)


@app.route('/about')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


# @app.after_request
# def add_header(response,methods=["POST","GET"]):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
    
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=600'
#     return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")