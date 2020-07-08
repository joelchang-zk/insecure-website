import hashlib
import json

from flask import Blueprint, redirect, render_template, request, url_for
from helper.generalfunctions import changePasswordActions, profileActions
from routes.common.__init__ import connection, ALLOWED_EXTENSIONS

common_blueprint = Blueprint('common','common', template_folder= 'templates')

@common_blueprint.route('/home/<string:username>/<string:role>')
def home(username, role):
    cursor = connection.cursor()
    query = "SELECT * from cookie where username = '" + str(username) + "';"
    cursor.execute(query)
    results = cursor.fetchall()
    for x in results:
        first = str(x[1])
        second = str(x[2])
    checkCookie = request.cookies.get(first)
    if first == '' or second == '':
        return redirect(url_for('login'))
    elif second != checkCookie:
        return redirect(url_for('login'))
    else:
        return render_template('home.html', username=username, role=role)


@common_blueprint.route('/<string:username>/logout')
def logout(username):
    cursor = connection.cursor()
    query = "UPDATE cookie set first = NULL,second = NULL WHERE username = '" + \
        str(username) + "';"
    cursor.execute(query)
    connection.commit()
    if 'A' in username:
        return redirect(url_for('general.adminLogin'))
    elif 'S' in username:
        return redirect(url_for('general.doctorLogin'))
    elif 'P' in username:
        return redirect(url_for('general.patientLogin'))
    else:
        return redirect(url_for('general.labTechLogin'))

@common_blueprint.route('/<string:username>/password/change/', methods=['GET', 'POST'])
def changePassword(username):
    cursor = connection.cursor()
    role = ""
    if 'S' in username:
        role = "doctor"
    elif 'P' in username:
        role = "patient"
    elif 'A' in username:
        role = "admin"
    else:
        role = "lab technician"
    getCurrentPasswordQuery = "SELECT password from users where username = '" + \
        str(username) + "';"
    cursor.execute(getCurrentPasswordQuery)
    results = json.loads(json.dumps(cursor.fetchall()))
    currentPass = results[0][0]
    print(currentPass)
    if request.method == 'POST':
        currentPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        repeatPassword = request.form['repeatPassword']
        print(len(currentPassword))
        print(len(newPassword))
        print(len(repeatPassword))
        hashedCurrentPassword = hashlib.md5(
            str(currentPassword).encode()).hexdigest()
        return changePasswordActions(hashedCurrentPassword, currentPass, repeatPassword, newPassword, cursor, connection, username, role)
    else:
        print("GET")
        return render_template('changepassword.html', username=username, role=role)


@common_blueprint.route('/<string:username>/profile', methods=['GET', 'POST'])
def profile(username):
    role = ""
    if 'S' in username:
        role = "doctor"
    elif 'P' in username:
        role = "patient"
    elif 'A' in username:
        role = "admin"
    else:
        role = "lab technician"
    cursor = connection.cursor()
    getDetailsQuery = "SELECT * from users where username = '" + str(username) + "';"
    cursor.execute(getDetailsQuery)
    results = json.loads(json.dumps(cursor.fetchall()))
    filedir = results[0][5]
    return profileActions(request, cursor, connection, username, ALLOWED_EXTENSIONS, results, role,filedir)
