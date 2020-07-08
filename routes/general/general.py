import hashlib
import json

from flask import Blueprint, redirect, render_template, request, url_for
from helper.generalfunctions import (checkAdminLogin, checkDoctorLogin,
                                     checkLabTechLogin, checkPatientLogin,
                                     commitEnquiry)
from routes.general.__init__ import connection

general_blueprint = Blueprint('general','general', template_folder= 'templates')

@general_blueprint.route('/')
def index():
    return render_template('index.html')

@general_blueprint.route('/contact')
def contact():
    return render_template('contactus.html')

@general_blueprint.route('/about')
def about():
        return render_template("about.html")

@general_blueprint.route('/doctors/list/', methods = ['GET', 'POST'])
def doctorsList():
    cursor = connection.cursor()
    doctorQuery = "SELECT * from users where role = 'doctor';"
    cursor.execute(doctorQuery)
    results = json.loads(json.dumps(cursor.fetchall()))
    if request.method == 'POST':
        query = request.form['queryName']
        print("POST")
        print(query)
        return redirect(url_for('searchDoctorQuery', query = query))
    else:
        return render_template('doctorslist.html', results = results)

@general_blueprint.route('/doctors/find/<string:query>/', methods = ['GET', 'POST'])
def searchDoctorQuery(query):
    cursor = connection.cursor()
    searchQuery = "SELECT * from users where role = 'doctor' and name LIKE '%" + str(query) + "%';"
    cursor.execute(searchQuery)
    searchResults = json.loads(json.dumps(cursor.fetchall()))
    print(searchResults)
    if len(searchResults) == 0:
        isEmpty = True
        return render_template('finddoctors.html', isEmpty = isEmpty)
    else:
        return render_template('finddoctors.html', searchResults = searchResults)

@general_blueprint.route('/general/enquiries/', methods = ['GET', 'POST'])
def generalEnquiries():
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        enquiry = request.form['enquiries'].strip()
        if len(name) == 0 or len(email) == 0 or len(enquiry) == 0:
            errorMessage = "Fields cannot be left empty!"
            return render_template('generalenquiries.html', errorMessage = errorMessage)
        else:
            commitEnquiry(name,email,enquiry, cursor, connection)
            successMessage = "Your enquiry has been successfully submitted!"
            return render_template('generalenquiries.html', successMessage = successMessage)
    return render_template('generalenquiries.html')

@general_blueprint.route('/login/doctor/', methods = ['GET', 'POST'])
def doctorLogin():
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashedPassword = hashlib.md5(str(password).encode())
        resultsQuery = "SELECT * from users where username = '" + \
            str(username) + "' AND password = '" + \
                str(hashedPassword.hexdigest()) + "';"
        cursor.execute(resultsQuery)
        results = cursor.fetchall()
        try:
            return checkDoctorLogin(results,cursor,connection, username)
        except Exception as e:
            print(e)
            error = "Invalid username/password"
            return render_template("login.html", error=error)
    else:
        return render_template('login.html')

@general_blueprint.route('/login/patient/', methods=['GET', 'POST'])
def patientLogin():
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashedPassword = hashlib.md5(str(password).encode())
        resultsQuery = "SELECT * from users where username = '" + \
            str(username) + "' AND password = '" + \
                str(hashedPassword.hexdigest()) + "';"
        cursor.execute(resultsQuery)
        results = cursor.fetchall()
        try:
            return checkPatientLogin(results, cursor, connection, username)
        except:
            error = "Invalid username/password"
            return render_template("login.html", error=error)
    else:
        return render_template('login.html')

@general_blueprint.route('/login/labTech/', methods=['GET', 'POST'])
def labTechLogin():
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashedPassword = hashlib.md5(str(password).encode())
        print(hashedPassword)
        resultsQuery = "SELECT * from users where username = '" + \
            str(username) + "' AND password = '" + \
                str(hashedPassword.hexdigest()) + "';"
        cursor.execute(resultsQuery)
        results = cursor.fetchall()
        print(results)
        try:
            return checkLabTechLogin(results, cursor, connection, username)
        except:
            error = "Invalid username/password"
            return render_template("login.html", error=error)
    else:
        return render_template('login.html')

@general_blueprint.route('/adminlogin/admin/admin', methods=['GET', 'POST'])
def adminLogin():
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashedPassword = hashlib.md5(str(password).encode())
        print(hashedPassword)
        resultsQuery = "SELECT * from users where username = '" + \
            str(username) + "' AND password = '" + \
                str(hashedPassword.hexdigest()) + "';"
        cursor.execute(resultsQuery)
        results = cursor.fetchall()
        print(results)
        try:
            return checkAdminLogin(results, cursor, connection, username)
        except:
            error = "Invalid username/password"
            return render_template("login.html", error=error)
    else:
        return render_template('login.html')
