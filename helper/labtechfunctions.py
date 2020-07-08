import os
from datetime import datetime

from flask import redirect, render_template, url_for

from helper.functions import allowed_file, encryptFileName, genRandomId


def LTUploadFiles(title,ALLOWED_EXTENSIONS, mri, cursor, connection, username):
    if len(title) == 0:
        errorMessage = "The title field must be filled. Please try again!"
        return render_template('LTuploads.html', username = username, errorMessage = errorMessage)
    elif str(mri.filename) == "":
        errorMessage = "You have not uploaded an MRI image. Please try again!"
        return render_template('LTuploads.html', username = username, errorMessage = errorMessage)
    elif allowed_file(mri.filename, ALLOWED_EXTENSIONS):
        fileName = encryptFileName(str(mri.filename))
        print(fileName)
        extension = "\\static\\LT\\" + str(username) + str(fileName)
        filedir = "/static/LT/" + str(username) + str(fileName)
        directory = str(os.getcwd()) + str(extension)
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(directory)
        formid = genRandomId()
        updateQuery = "INSERT INTO files(picdir,username,formid,title, entrydate) VALUES('" + str(filedir) + "','" + str(username) + "','" + str(formid) + "','" + str(title) + "','" + str(current_time) + "');"
        cursor.execute(updateQuery)
        connection.commit()
        mri.save(directory)
        successMessage = "Files have been successfully uploaded."
        return render_template('LTuploads.html', username = username, successMessage = successMessage)
