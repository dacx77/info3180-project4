
"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField # other fields include PasswordField 
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


class ProfileForm(Form):
     name = TextField('Name', validators=[Required()])
     email = TextField('Email', validators=[Required()])
     password = TextField('Password', validators=[Required()])
     
#    
###
# Routing for your application.
###
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
            currentUser = profile.email
            session['currentUser'] = currentUser
            return redirect(url_for('home', currentUser=currentUser))
    return render_template('login.html', form=form)
    
@app.route("/logout")

def logout():
    logout_user()
    return render_template('logout.html')
                           
@app.route('/api/thumbnail/process')
def home():
    """Render website's home page."""
    currentUser = request.args['currentUser']  
    currentUser = session['currentUser']
    return render_template('home.html', currentUser = currentUser)

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
    
@app.route('/urladd', methods=['POST','GET'])    
def urlAdd():
    if request.method == "POST":
          
        currentUser = session['currentUser']
        url_chosen = request.form['thumb']
        profile = myprofile.query.filter(myprofile.email == currentUser).first()
        
        profile.url = url_chosen
        
    return render_template('url_added.html', url_chosen=url_chosen)
    
    

@app.route('/api/user/register', methods=['POST','GET'])
def profile_add():
    import os
    from flask import Flask, request, redirect, url_for
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        
        
        # write the information to the database
        newprofile = myprofile(name=name,email=email,password=password, url = "")
        db.session.add(newprofile)
        db.session.commit()

        return "Name: {} with email: {} was created.".format(request.form['name'],request.form['email'])

    form = ProfileForm()
    return render_template('profile_add.html',form=form)

@app.route('/profiles',methods=["POST","GET"])
@login_required
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
        return jsonify({"id":profile.id, "email":profile.email})
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


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")