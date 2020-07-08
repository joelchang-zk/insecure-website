from flask import Flask, request, jsonify
from ..setup import setUpDB

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd2\x04S4\xbc\xce\xe2\x17\xfb\xff\x19C@\xa6e\xc2\xf4\x18\xad\xe8\xc4\xcb'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

connection = setupDB()
print("DB SET UP")
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
