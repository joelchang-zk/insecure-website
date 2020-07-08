import hashlib
import json

from flask import Blueprint, redirect, render_template, request, url_for

from helper.functions import JSONSerialConvertor
from helper.labtechfunctions import LTUploadFiles
from routes.labtech.__init__ import ALLOWED_EXTENSIONS, connection

labtech_blueprint =  Blueprint('labtech', 'labtech', template_folder= 'templates')

@labtech_blueprint.route('/<string:username>/LT/documents', methods = ['GET', 'POST'])
def LTHomePage(username):
    cursor = connection.cursor()
    getRecordQuery = "SELECT * from files where username = '" + str(username) + "';"
    cursor.execute(getRecordQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    return render_template('LThomepage.html', username = username, results = results)

@labtech_blueprint.route('/<string:username>/LT/documents/upload/', methods = ['GET', 'POST'])
def  LTuploads(username):
    cursor = connection.cursor()
    if request.method == 'POST':
        print("POST")
        title = request.form['fileTitle']
        mri = request.files['profileImage']
        print(title)
        print(mri)
        return LTUploadFiles(title,ALLOWED_EXTENSIONS, mri, cursor, connection, username)
    else:
        return render_template('LTuploads.html', username = username)

@labtech_blueprint.route('/<string:username>/LT/documents/<string:formid>/', methods = ['GET', 'POST'])
def viewMRI(username, formid):
    cursor = connection.cursor()
    checkQuery = "SELECT * from files where formid = '" + str(formid) + "';"
    cursor.execute(checkQuery)
    results = json.loads(json.dumps(cursor.fetchall(), default=JSONSerialConvertor))
    return render_template('MRI.html', username = username, results = results)
