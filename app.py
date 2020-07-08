from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd2\x04S4\xbc\xce\xe2\x17\xfb\xff\x19C@\xa6e\xc2\xf4\x18\xad\xe8\xc4\xcb'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.route('/', methods = ['GET','POST'])
def index():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=False, port=5300)
    
