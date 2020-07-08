from flask import Flask, request, jsonify
from helper.setup import setUpDB
from routes.general import general
from routes.doctor import doctor
from routes.common import common
from routes.patient import patient
from routes.labtech import labtech
from routes.admin import admin

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd2\x04S4\xbc\xce\xe2\x17\xfb\xff\x19C@\xa6e\xc2\xf4\x18\xad\xe8\xc4\xcb'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.register_blueprint(general.general_blueprint)
app.register_blueprint(doctor.doctor_blueprint)
app.register_blueprint(common.common_blueprint)
app.register_blueprint(patient.patient_blueprint)
app.register_blueprint(labtech.labtech_blueprint)
app.register_blueprint(admin.admin_blueprint)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
